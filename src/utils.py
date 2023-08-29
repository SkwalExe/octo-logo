import os
from PIL import Image, ImageDraw, ImageFont, ImageColor

def get_text_size(text, font):
    text_bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0))).textbbox(
        (0, 0), text, font=font
    )
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    return text_width, text_height


def get_font_height(font):
    return font.getsize("azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQASDFGHJKLMWXCVBN")[1]


def remove_ext(filename):
    return filename.split(".")[0]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
COLORS_DIR = os.path.join(BASE_DIR, "colors")

# Get all the fonts in the fonts directory
font_list = os.listdir(FONTS_DIR)

# Get all the color schemes in the colors directory
# keep only files with the .toml extension
# and remove the extension
color_list = [
    remove_ext(color) for color in os.listdir(COLORS_DIR) if color.endswith(".toml")
]