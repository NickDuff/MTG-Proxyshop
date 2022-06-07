"""
GUI Functions
Console Display
"""

import ctypes
import os
import random
import sys
import time
import asynckivy as ak
from datetime import datetime as dt
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.utils import get_color_from_hex
from proxyshop.core import (
    check_for_updates,
    update_template,
    authenticate_user,
    check_for_authentication
)
from proxyshop.settings import cfg
cwd = os.getcwd()


"""
CONSOLE MODULES
"""


class Console (BoxLayout):
    """
    Main console class
    """
    def __init__(self, **kwargs):
        Builder.load_file(os.path.join(cwd, "proxyshop/console.kv"))
        super().__init__(**kwargs)

    def update(self, msg="", e=None, end="\n"):
        """
        Add text to console
        """
        output = self.ids.console_output
        output.text += msg+end
        self.ids.viewport.scroll_y = 0
        if e: self.log_exception(e)

    def log_error(self, msg, card, template=None, e=None):
        """
        Log failed card in tmp
        Then prompt error request
        """
        cur_time = dt.now().strftime("%m/%d/%Y %H:%M")
        if template: log_text = f"{card} ({template}) [{cur_time}]\n"
        else: log_text = f"{card} [{cur_time}]\n"
        with open(os.path.join(cwd, "tmp/failed.txt"), "a", encoding="utf-8") as log:
            log.write(log_text)
        return self.error(msg, e)

    def error(self, msg, e=None, color=True, continue_msg="Continue to next card?"):
        """
        Display error, wait for user to cancel or continue.
        """
        # End waiting to cancel
        self.end_await()

        # Notify user
        if not cfg.skip_failed:
            if color: self.update(f"[color=#a84747]{msg}[/color]\nContinue to next card?")
            else: self.update(f"{msg}\n{continue_msg}")
        else: self.update(f"[color=#a84747]{msg}[/color]\nContinuing to next card!")

        # Log exception if given
        if e: self.log_exception(e)

        # Enable buttons
        self.ids.continue_btn.disabled = False
        self.ids.cancel_btn.disabled = False

        # Prompt user response
        if cfg.skip_failed: result = True
        else: result = self.ids.console_controls.wait()

        # Cancel or don't
        if not result: self.update("Understood! Canceling render operation.")

        # Disable buttons
        self.ids.continue_btn.disabled = True
        self.ids.cancel_btn.disabled = True
        return result

    def wait(self, msg):
        """
        Wait for user to continue.
        """
        self.end_await()
        self.update(msg)
        self.ids.continue_btn.disabled = False
        self.ids.console_controls.wait()
        self.ids.continue_btn.disabled = True
        return True

    def await_cancel(self, thr):
        """
        Await for user to cancel the operation.
        Auto-returns if the render finishes.
        """
        self.ids.console_controls.success = False
        self.ids.cancel_btn.disabled = False
        self.ids.console_controls.await_cancel()
        if not self.ids.console_controls.success:
            self.ids.cancel_btn.disabled = True
            App.get_running_app().enable_buttons()
            self.kill_thread(thr)
            self.update("Canceling render process!\n")
            sys.exit()
        else: return True

    def end_await(self):
        """
        Ends the await cancel loop
        """
        self.ids.console_controls.success = True
        self.ids.console_controls.running = False
        self.ids.cancel_btn.disabled = True

    @staticmethod
    def log_exception(e):
        """
        Log python exception.
        """
        cur_time = dt.now().strftime("%m/%d/%Y %H:%M")
        if hasattr(e, '__traceback__'):
            e = f"[{cur_time}] Line: {e.__traceback__.tb_lineno}\n" \
                f"{e.__traceback__.tb_frame.f_code.co_filename}: {e}\n"
        with open(os.path.join(cwd, "tmp/error.txt"), "a", encoding="utf-8") as log:
            log.write(e)

    @staticmethod
    def kill_thread(thr):
        """
        Kill current render thread.
        @param thr: threading.Thread object
        """
        thread_id = thr.ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1: ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)


class ConsoleOutput (Label):
    """
    Label displaying console output
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ConsoleControls (BoxLayout):
    """
    Console control buttons
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = True
        self.waiting = False
        self.success = True
        self.choice = False

    def wait(self):
        """
        Force wait until user makes a choice
        """
        self.waiting = True
        while self.waiting:
            time.sleep(.5)
        return self.choice

    def choose(self, confirm=True):
        """
        Define the response, end wait
        """
        if confirm: self.choice = True
        else:
            self.choice = False
            self.running = False
            self.success = False
        self.waiting = False

    def await_cancel(self):
        """
        Await for user cancelling during render process
        """
        self.running = True
        while self.running:
            time.sleep(1)
        return None

    @staticmethod
    async def check_for_updates():
        """
        Open updater Popup.
        """
        while True:
            if check_for_authentication():
                # We are Authenticated
                Updater = UpdatePopup()
                Updater.open()
                await ak.run_in_thread(Updater.check_for_updates, daemon=True)
                ak.start(Updater.populate_updates())
                break
            else:
                # We need to authenticate
                auth = Authenticator()
                auth.open()
                success = await ak.run_in_thread(auth.authenticate, daemon=True)
                await ak.sleep(2)
                auth.dismiss()
                if success: continue
                else: break

"""
Updater
"""


class UpdatePopup(Popup):
    """
    Popup modal for updating templates.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading = True
        self.updates = {}
        self.categories = {}
        self.entries = {}

    def check_for_updates(self):
        """
        Runs the check_for_updates core function, then lists needed updates.
        """
        self.updates = check_for_updates()

    async def populate_updates(self):
        """
        Load the list of updates available.
        """
        # Binary tracker for alternating color
        chk = 0

        # Remove loading screen
        if self.loading:
            self.ids.container.remove_widget(self.ids.loading)
            self.ids.container.padding = [0, 0, 0, 0]
            self.loading = False

        # Loop through categories
        for cat, temps in self.updates.items():

            # Loop through updates within this category
            for i, temp in enumerate(temps):
                # Alternate table item color
                if chk == 0: chk, bg_color = 1, "#101010"
                else: chk, bg_color = 0, "#181818"
                self.entries[temp['id']] = UpdateEntry(self, temp, bg_color)
                self.ids.container.add_widget(self.entries[temp['id']])

        # Remove loading text
        if len(self.updates) == 0:
            self.ids.loading_text.text = " [i]No updates found![/i]"
        else: self.ids.loading_text.text = " [i]Updates Available[/i]"


class UpdateEntry(BoxLayout):
    def __init__(self, parent, temp, bg_color, **kwargs):
        if temp['plugin']: plugin = f" [size=18]({temp['plugin']})[/size]"
        else: plugin = ""
        self.bg_color = bg_color
        self.name = f"{temp['type']} - {temp['name']}{plugin}"
        self.status = f"[color=#59d461]{temp['version_new']}[/color]"
        self.data = temp
        self.root = parent
        super().__init__(**kwargs)

    async def download_update(self, download):
        self.progress = ProgressBar()
        download.clear_widgets()
        download.add_widget(self.progress)
        await ak.run_in_thread(lambda: update_template(self.data, self.update_progress), daemon=True)
        await ak.sleep(.5)
        self.root.ids.container.remove_widget(self.root.entries[self.data['id']])

    def update_progress(self, tran, total):
        if self.progress.value != 100:
            self.progress.value += 5


"""
Authenticator
"""


class Authenticator(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def authenticate(self):
        if authenticate_user():
            self.ids.response.text = "[b]Authentication: SUCCESS![/b]"
            return True
        else:
            self.ids.response.text = "[b]Authentication: FAILED![/b]"
            return False


"""
UTILITY FUNCTIONS
"""


def get_font(name, default="Roboto"):
    """
    Instantiate font if exists, otherwise return False
    """
    basename = name[0:-4]
    try:
        LabelBase.register(name=basename, fn_regular=name)
        return basename
    except OSError:
        try:
            LabelBase.register(name=basename, fn_regular=f"fonts/{name}")
            return basename
        except OSError:
            try:
                LabelBase.register(
                    name=basename,
                    fn_regular=f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows\\Fonts\\{name}"
                )
                return basename
            except OSError: return default


"""
UTILITY CLASSES
"""


class HoverBehavior(object):
    """
    Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If I have no parent
        pos = args[1]
        # Next line to_widget allowed to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')


class HoverButton(Button, HoverBehavior):
    """
    Animated button to run new render operation
    """
    font_name = get_font("Beleren Small Caps.ttf")
    options = [
            "Do it!", "Let's GO!", "Ready?",
            "PROXY", "Hurry up!", "GAME ON",
            "Let's DUEL", "Prox it up!", "Go for it!"
    ]
    hover_color = "#a4c5eb"
    org_text = None
    org_color = None

    def on_enter(self):
        """
        When hovering
        """
        if not self.disabled:
            Window.set_system_cursor('hand')
            self.org_text = self.text
            self.org_color = self.background_color
            self.text = random.choice(self.options)
            self.background_color = get_color_from_hex(self.hover_color)

    def on_leave(self):
        """
        When leave
        """
        if self.org_text:
            Window.set_system_cursor('arrow')
            self.text = self.org_text
            self.background_color = self.org_color


console_handler = Console()