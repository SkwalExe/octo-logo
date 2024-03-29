from wizard import TextQuestion, SelectQuestion
from textual.validation import Number
from utils import font_list, color_scheme_names, FONTS_DIR, color_schemes, os, get_font_height, get_text_size
from PIL import Image, ImageDraw, ImageFont, ImageColor
import sys

sys.path.append("..")


questions = [
    SelectQuestion("font", "Select a font", [(font, font) for font in font_list], "Iosevka-Nerd-Font-Complete.ttf"),
    SelectQuestion("color", "Select a color scheme", color_scheme_names, "adi1090x"),
    TextQuestion("padding_x", "Padding x (px)", [Number()], "200", "200"),
    TextQuestion("padding_y", "Padding y (px)", [Number()], "20", "20"),
    TextQuestion("gap", "Gap between text and bar (px)", [Number()], "20", "20"),
    TextQuestion("bar_size", "Bar weight (px)", [Number()], "20", "20"),
    TextQuestion("additionnal_bar_width", "Additionnal bar width (px)", [Number()], "20", "20"),
]

active = False


def get_image(answers, type):
    if type not in ['all', 'first_letter']:
        raise ValueError("Invalid type")

    # Load the selected font
    font_size = 500
    font = ImageFont.truetype(os.path.join(FONTS_DIR, answers["font"]), font_size)

    background = ImageColor.getrgb(color_schemes[answers['color']]["background"])
    text = ImageColor.getrgb(color_schemes[answers['color']]["text"])
    accent = ImageColor.getrgb(color_schemes[answers['color']]["accent"])

    # Get the width and height of the texts
    text_width, text_height = get_text_size(answers['name'], font)
    font_height = get_font_height(font)

    # Get the correct image width and height
    image_width = 2 * int(answers['padding_x']) + text_width
    image_height = 2 * int(answers['padding_y']) + font_height

    # Create the image
    image = Image.new("RGB", (image_width, image_height), background)
    draw = ImageDraw.Draw(image)

    # Get the anchor position and type
    anchor_type = "lm"
    anchor_x = int(answers['padding_x'])
    anchor_y = image_height / 2 - (int(answers['gap']) + int(answers['bar_size'])) / 2

    anchor_pos = (anchor_x, anchor_y)

    # Get the bbox of the first letter

    first_letter_bbox = draw.textbbox(
        anchor_pos, answers['name'][0], font=font, anchor=anchor_type
    )

    # Get the underline position
    underline_start_x = first_letter_bbox[0] - int(answers['additionnal_bar_width'])
    underline_start_y = first_letter_bbox[3] + int(answers['gap'])

    # The end of the underline depends on the type
    # If the type is 'all', the underline will go from the start of the first letter to the end of the text
    # If the type is 'first_letter', the underline will go
    # from the start of the first letter to the end of the first letter
    if type == 'first_letter':
        underline_end_x = int(answers['additionnal_bar_width']) + (first_letter_bbox[2])
    else:
        underline_end_x = int(int(answers['padding_x']) + text_width)

    underline_end_y = underline_start_y + int(answers['bar_size'])

    underline_start = (underline_start_x, underline_start_y)
    underline_end = (underline_end_x, underline_end_y)

    underline_pos = [underline_start, underline_end]

    # Underline the first letter
    draw.rectangle(underline_pos, fill=accent, width=answers['bar_size'])

    # Draw the text
    draw.text(
        anchor_pos,
        answers['name'],
        font=font,
        fill=text,
        anchor=anchor_type,
    )

    # Redraw the first letter
    draw.text(
        anchor_pos,
        answers['name'][0],
        font=font,
        fill=accent,
        anchor=anchor_type,
    )

    return image
