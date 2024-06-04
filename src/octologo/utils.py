import os
from importlib import import_module
from sys import stdout
from time import time
from types import ModuleType
from typing import Any

import toml
from loguru import logger
from PIL import Image, ImageDraw
from PIL.ImageFont import FreeTypeFont

logger.remove()
logger.add(
    stdout,
    format="[ <green>{time:HH:mm:ss}</green> ]" " - <level>{level}</level> -> " "<level>{message}</level>",
)


def get_text_size(text: str, font: FreeTypeFont) -> tuple[int, int]:
    text_bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0))).textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    return text_width, text_height


def get_font_height(font: FreeTypeFont) -> int:
    return font.getbbox("azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQASDFGHJKLMWXCVBN0123456789")[3]


def remove_ext(filename: str) -> str:
    """
    Remove the extension from a filename if there is one
    """
    return filename.split(".")[0]


class Style:
    display_name: str
    module: ModuleType

    def __init__(self, display_name: str, module: ModuleType) -> None:
        self.display_name = display_name
        self.module = module


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
COLORS_DIR = os.path.join(BASE_DIR, "colors")


# Get all the fonts in the fonts directory
def get_font_list() -> list[str]:
    return os.listdir(FONTS_DIR)


font_list = get_font_list()


# Get all the color schemes in the colors directory
# keep only files with the .toml extension
# and remove the extension
def get_color_schemes() -> dict[str, dict[str, str]]:
    colors = dict()
    for color_file_name in os.listdir(COLORS_DIR):
        # Only keep .toml files
        if not color_file_name.endswith(".toml"):
            continue

        color_parsed = toml.load(os.path.join(COLORS_DIR, color_file_name))

        colors[remove_ext(color_file_name)] = color_parsed

    return colors


color_schemes = get_color_schemes()
color_scheme_names: list[tuple[str, Any]] = [
    (color_schemes[color_scheme]["name"], color_scheme) for color_scheme in color_schemes
]


def get_styles() -> dict[str, Style]:
    """
    return an array of style_id => Style {.module, .display_name}
    """
    # Load the styles in the styles directory
    styles = dict()
    for style in os.listdir(os.path.join(BASE_DIR, "styles")):
        # Only keep .py files
        if not style.endswith(".py"):
            continue

        module = import_module(f"octologo.styles.{remove_ext(style)}")

        # Only keep files with the active attribute set to True
        # This allows to ignore some scripts that may be in the styles directory
        if not module.active:
            continue

        styles[remove_ext(style)] = Style(module.display_name, module)

    return styles


def get_output_filename(project_name: str) -> str:
    return f"octologo_{project_name}_{int(time())}.png"


styles = get_styles()

style_names: list[tuple[str, Any]] = [(styles[style].display_name, style) for style in styles]
