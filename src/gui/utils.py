"""
GUI UTILITIES
"""
# Standard Library Imports
import os
import random

# Third Party Imports
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex

# Local Imports
from src.core import card_types

"""
UTILITY FUNCTIONS
"""


def get_font(name: str, default: str = "Roboto"):
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
            except OSError:
                return default


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

    """
    BLANK METHODS - Overwritten by Extend Class, e.g. Button
    """

    def dispatch(self, action):
        return

    @staticmethod
    def collide_point(point: float):
        if point:
            return True
        return False

    @staticmethod
    def to_widget(point: list):
        return point

    @staticmethod
    def get_root_window():
        return App.root_window

    @staticmethod
    def register_event_type(event: str):
        return


class HoverButton(Button, HoverBehavior):
    """
    Animated button to run new render operation
    """
    options = [
            "Do it!", "Let's GO!", "Ready?",
            "PROXY", "Hurry up!", "GAME ON",
            "Let's DUEL", "Prox it up!", "Go for it!"
    ]
    hover_color = "#a4c5eb"
    org_text = None
    org_color = None

    def __init__(self, **kwargs):
        # Set the default font
        self.font_name = get_font("Beleren Small Caps.ttf")
        super().__init__(**kwargs)

    def on_enter(self):
        """
        When hovering
        """
        if not self.disabled:
            self.org_color = self.background_color
            if len(self.options) > 0:
                self.org_text = self.text
                self.text = random.choice(self.options)
            self.background_color = get_color_from_hex(self.hover_color)

    def on_leave(self):
        """
        When leave
        """
        if self.org_color:
            self.background_color = self.org_color
            if len(self.options) > 0:
                self.text = self.org_text


"""
RESOURCES
"""


class GUIResources:
    def __init__(self):
        self.template_row: dict[str, dict[str, BoxLayout]] = {k: {} for k in card_types}
        self.template_btn: dict[str, dict[str, ToggleButton]] = {k: {} for k in card_types}
        self.template_btn_cfg: dict[str, dict[str, Button]] = {k: {} for k in card_types}


GUI = GUIResources()
