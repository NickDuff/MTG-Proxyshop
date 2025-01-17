"""
MRTEFERI TEMPLATES
"""
from functools import cached_property
from typing import Optional, Callable

from actions import pencilsketch, sketch
import src.templates as temp
from src.settings import cfg
import src.helpers as psd
from src.utils.enums_layers import LAYERS

from photoshop.api._artlayer import ArtLayer
import photoshop.api as ps
app = ps.Application()


"""
NORMAL TEMPLATES
"""


class SketchTemplate (temp.NormalTemplate):
    """
    Sketch showcase from MH2
    Original PSD by Nelynes
    """
    template_suffix = "Sketch"

    @property
    def name_shifted(self) -> bool:
        return False

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_companion(self) -> bool:
        return False

    @property
    def art_action(self) -> Optional[Callable]:
        action = cfg.get_setting(
            section="ACTION",
            key="Sketch.Action",
            default="Advanced Sketch",
            is_bool=False
        )
        if action == "Advanced Sketch":
            return pencilsketch.run
        if action == "Quick Sketch":
            return sketch.run
        return

    @property
    def art_action_args(self) -> Optional[dict]:
        if not self.art_action == pencilsketch.run:
            return
        return {
            'thr': self.event,
            'rough_sketch': cfg.get_setting(
                section="ACTION",
                key="Rough.Sketch.Lines",
                default=False
            ),
            'draft_sketch': cfg.get_setting(
                section="ACTION",
                key="Draft.Sketch.Lines",
                default=False
            ),
            'black_and_white': cfg.get_setting(
                section="ACTION",
                key="Black.And.White",
                default=False
            ),
            'manual_editing': cfg.get_setting(
                section="ACTION",
                key="Sketch.Manual.Editing",
                default=False
            )
        }


class KaldheimTemplate (temp.NormalTemplate):
    """
    Kaldheim viking legendary showcase.
    Original Template by FeuerAmeise
    """
    template_suffix = "Kaldheim"

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_legendary(self) -> bool:
        return False

    @property
    def twins_layer(self) -> Optional[ArtLayer]:
        return

    @property
    def background_layer(self) -> Optional[ArtLayer]:
        return

    @cached_property
    def pt_layer(self) -> Optional[ArtLayer]:
        if "Vehicle" in self.layout.type_line:
            return psd.getLayer("Vehicle", LAYERS.PT_BOX)
        return psd.getLayer(self.twins, LAYERS.PT_BOX)

    @cached_property
    def pinlines_layer(self) -> Optional[ArtLayer]:
        if self.is_land:
            return psd.getLayer(self.pinlines, LAYERS.LAND_PINLINES_TEXTBOX)
        if "Vehicle" in self.layout.type_line:
            return psd.getLayer("Vehicle", LAYERS.PINLINES_TEXTBOX)
        return psd.getLayer(self.pinlines, LAYERS.PINLINES_TEXTBOX)


class CrimsonFangTemplate (temp.NormalTemplate):
    """
    The crimson vow showcase template.
    Original template by michayggdrasil
    Works for Normal and Transform cards
    Transform is kinda experimental.
    """
    template_suffix = "Fang"

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_companion(self) -> bool:
        return False

    @property
    def background(self):
        return self.pinlines

    @cached_property
    def pinlines_layer(self) -> Optional[ArtLayer]:
        # Pinlines
        if self.is_land:
            return psd.getLayer(self.pinlines, LAYERS.LAND_PINLINES_TEXTBOX)
        if self.name_shifted and not self.is_front:
            return psd.getLayer(self.pinlines, "MDFC " + LAYERS.PINLINES_TEXTBOX)
        return psd.getLayer(self.pinlines, LAYERS.PINLINES_TEXTBOX)

    @cached_property
    def transform_icon(self) -> Optional[ArtLayer]:
        if self.name_shifted and self.is_front:
            return psd.getLayer("tf-front", self.text_layers)
        elif self.name_shifted:
            return psd.getLayer("tf-back", self.text_layers)
        return

    def enable_frame_layers(self):
        super().enable_frame_layers()

        # Add transform if necessary
        if self.name_shifted and self.transform_icon:
            psd.getLayer("Button", self.text_layers).visible = True
            self.transform_icon.visible = True


class PhyrexianTemplate (temp.NormalTemplate):
    """
    From the Phyrexian secret lair promo
    """
    template_suffix = "Phyrexian"

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_companion(self) -> bool:
        return False

    @property
    def twins_layer(self) -> Optional[ArtLayer]:
        return

    @property
    def background_layer(self) -> Optional[ArtLayer]:
        return


class DoubleFeatureTemplate (temp.NormalTemplate):
    """
    Midnight Hunt / Vow Double Feature Showcase
    Original assets from Warpdandy's Proximity Template
    Doesn't support companion, nyx, or twins layers.
    """
    template_suffix = "Double Feature"

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_companion(self) -> bool:
        return False

    @property
    def twins_layer(self) -> Optional[ArtLayer]:
        return

    @property
    def pinlines_layer(self) -> Optional[ArtLayer]:
        return

    @property
    def background_layer(self) -> Optional[ArtLayer]:
        return psd.getLayer(self.layout.pinlines, LAYERS.BACKGROUND)


class MaleMPCTemplate (temp.NormalTemplate):
    """
    MaleMPC's extended black box template.
    """
    template_suffix = "Extended Black"

    @cached_property
    def pinlines_layer_bottom(self) -> Optional[ArtLayer]:
        if self.is_land:
            return psd.getLayer(self.pinlines, "Lower Land Pinlines")
        return psd.getLayer(self.pinlines, "Lower Pinlines")

    def enable_frame_layers(self):

        # Hide pinlines and shadow if legendary
        super().enable_frame_layers()

        # Lower pinlines
        self.pinlines_layer_bottom.visible = True

        # Content aware fill
        psd.content_fill_empty_area(self.art_layer)

    def enable_crown(self):
        psd.enable_mask(psd.getLayer(LAYERS.SHADOWS))
        psd.enable_mask(self.pinlines_layer.parent)
        super().enable_crown()


"""
CLASSIC TEMPLATE VARIANTS
"""


class ColorshiftedTemplate (temp.NormalTemplate):
    """
    Planar Chaos era colorshifted template
    Rendered from CC and MSE assets. Most titleboxes are built into pinlines.
    Doesn't support special layers for nyx, companion, land, or colorless.
    """
    template_suffix = "Shifted"

    def __init__(self, layout):
        cfg.real_collector = False
        super().__init__(layout)

    @cached_property
    def twins_layer(self) -> Optional[ArtLayer]:
        if "Artifact" in self.layout.type_line and self.pinlines != "Artifact":
            if self.is_legendary:
                return psd.getLayer("Legendary Artifact", "Twins")
            return psd.getLayer("Normal Artifact", "Twins")
        elif "Land" in self.layout.type_line:
            if self.is_legendary:
                return psd.getLayer("Legendary Land", "Twins")
            return psd.getLayer("Normal Land", "Twins")
        return

    @cached_property
    def pt_layer(self) -> Optional[ArtLayer]:
        if self.is_creature:
            # Check if vehicle
            if "Vehicle" in self.layout.type_line:
                return psd.getLayer("Vehicle", LAYERS.PT_BOX)
            return psd.getLayer(self.twins, LAYERS.PT_BOX)
        return psd.getLayerSet(LAYERS.PT_BOX)

    @property
    def is_nyx(self) -> bool:
        return False

    @property
    def is_companion(self) -> bool:
        return False

    @property
    def is_land(self) -> bool:
        return False

    @property
    def is_colorless(self) -> bool:
        return False

    def enable_frame_layers(self):

        # White brush and artist for black border
        if self.layout.pinlines[0:1] == "B" and len(self.pinlines) < 3:
            psd.getLayer("Artist", self.legal_group).textItem.color = psd.rgb_white()
            psd.getLayer("Brush B", self.legal_group).visible = False
            psd.getLayer("Brush W", self.legal_group).visible = True

        super().enable_frame_layers()


"""
BASIC LAND TEMPLATES
"""


class BasicLandDarkMode (temp.BasicLandTemplate):
    """
    Basic land Dark Mode
    Credit to Vittorio Masia (Sid)
    """
    template_suffix = "Dark"

    def collector_info(self):
        # Collector info only has artist
        psd.replace_text(psd.getLayer(LAYERS.ARTIST, self.legal_group), "Artist", self.layout.artist)

    def load_artwork(self):
        super().load_artwork()

        # Content aware fill
        psd.content_fill_empty_area(self.art_layer)
