import toml
from PIL import Image, ImageDraw, ImageFont, ImageColor
import inquirer as inq

import sys
sys.path.append("..")

from utils import *

active = False

def get_image(name, type):
    if not type in ['all', 'first_letter']:
        raise ValueError("Invalid type")
    
    questions = [ 
        inq.List("font", message="Select a font", choices=font_list),
        inq.List("color", message="Select a color scheme", choices=color_list, default="adi1090x"),
        inq.Text("padding_x", message="Padding x (px)", default=200),
        inq.Text("padding_y", message="Padding y (px)", default=20),
        inq.Text(
            "gap", message="Gap between the first letter and the bar (px)", default=20
        ),
        inq.Text("bar_size", message="Bar size (px)", default=20),
        inq.Text(
            "additionnal_bar_width", message="Addionnal bar width (px)", default=5
        ),
    ]

    answers = inq.prompt(questions)

    # Convert the answers to integers
    try:
        padding_x = int(answers["padding_x"])
        padding_y = int(answers["padding_y"])
        gap = int(answers["gap"])
        bar_size = int(answers["bar_size"])
        additionnal_bar_width = int(answers["additionnal_bar_width"])
    except ValueError:
        print("px values must be integer")
        exit(1)

    # Load the selected font
    font_size = 500
    font = ImageFont.truetype(os.path.join(FONTS_DIR, answers["font"]), font_size)

    # Load the selected color scheme
    color_scheme_file = os.path.join(COLORS_DIR, f'{answers["color"]}.toml')
    color_scheme = toml.load(color_scheme_file)

    background = ImageColor.getrgb(color_scheme["background"])
    text = ImageColor.getrgb(color_scheme["text"])
    accent = ImageColor.getrgb(color_scheme["accent"])

    # Get the width and height of the texts
    text_width, text_height = get_text_size(name, font)
    font_height = get_font_height(font)

    # Get the correct image width and height
    image_width = 2 * padding_x + text_width
    image_height = 2 * padding_y + font_height

    # Create the image
    image = Image.new("RGB", (image_width, image_height), background)
    draw = ImageDraw.Draw(image)

    # Get the anchor position and type
    anchor_type = "lm"
    anchor_x = padding_x
    anchor_y = image_height / 2 - (gap + bar_size) / 2

    anchor_pos = (anchor_x, anchor_y)

    # Get the bbox of the first letter

    first_letter_bbox = draw.textbbox(
        anchor_pos, name[0], font=font, anchor=anchor_type
    )

    # Get the underline position
    underline_start_x = first_letter_bbox[0] - additionnal_bar_width
    underline_start_y = first_letter_bbox[3] + gap

    # The end of the underline depends on the type
    # If the type is 'all', the underline will go from the start of the first letter to the end of the text
    # If the type is 'first_letter', the underline will go from the start of the first letter to the end of the first letter
    underline_end_x = additionnal_bar_width + (first_letter_bbox[2] if type == 'first_letter' else padding_x + text_width)
    underline_end_y = underline_start_y + bar_size

    underline_start = (underline_start_x, underline_start_y)
    underline_end = (underline_end_x, underline_end_y)

    underline_pos = [underline_start, underline_end]

    # Underline the first letter
    draw.rectangle(underline_pos, fill=accent, width=bar_size)


    # Draw the text
    draw.text(
        anchor_pos,
        name,
        font=font,
        fill=text,
        anchor=anchor_type,
    )

    # Redraw the first letter
    draw.text(
        anchor_pos,
        name[0],
        font=font,
        fill=accent,
        anchor=anchor_type,
    )

    
    return image
