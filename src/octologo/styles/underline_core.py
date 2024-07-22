from octologo.utils import (
    FONTS_DIR,
    color_scheme_names,
    color_schemes,
    font_list,
    get_font_height,
    get_text_size,
    os,
)
from PIL import Image, ImageColor, ImageDraw, ImageFont
from PIL.Image import Image as ImageClass
from PIL.ImageFont import FreeTypeFont
from textual.validation import Number
from textual_wizard.inputs import Select, Text

questions = [
    Select(
        "font",
        "Select a font",
        options=[(font, font) for font in font_list],
        default_value="Iosevka-Nerd-Font-Complete.ttf",
    ),
    Select("color", "Select a color scheme", options=color_scheme_names, default_value="adi1090x"),
    Text("underline_count", "Lettrs to undrline", validators=[Number(minimum=0)], initial_value="1", placeholder="1"),
    Text("padding_x", "Padding x (px)", validators=[Number()], initial_value="200", placeholder="200"),
    Text("padding_y", "Padding y (px)", validators=[Number()], initial_value="20", placeholder="20"),
    Text("gap", "Gap between text and bar (px)", validators=[Number()], initial_value="20", placeholder="20"),
    Text("bar_size", "Bar weight (px)", validators=[Number()], initial_value="20", placeholder="20"),
    Text(
        "additionnal_bar_width",
        "Additionnal bar width (px)",
        validators=[Number()],
        initial_value="20",
        placeholder="20",
    ),
]

active = False


def get_image(answers: dict) -> ImageClass:
    # Load the selected font
    font_size = 500
    font: FreeTypeFont = ImageFont.truetype(os.path.join(FONTS_DIR, answers["font"]), font_size)

    # Set the colors
    background = ImageColor.getrgb(color_schemes[answers["color"]]["background"])
    text = ImageColor.getrgb(color_schemes[answers["color"]]["text"])
    accent = ImageColor.getrgb(color_schemes[answers["color"]]["accent"])

    # Get the width and height of the texts
    text_width = get_text_size(answers["name"], font)[0]
    font_height = get_font_height(font)

    # Get the correct image width and height
    image_width = 2 * int(answers["padding_x"]) + text_width
    image_height = 2 * int(answers["padding_y"]) + font_height

    # Create the image
    image = Image.new("RGB", (image_width, image_height), background)
    draw = ImageDraw.Draw(image)

    # Get the text anchor type and position on the image (where the text will be drawn)
    # LM = Left/Middle
    anchor_type = "lm"
    anchor_x = int(answers["padding_x"])
    anchor_y = image_height / 2 - (int(answers["gap"]) + int(answers["bar_size"])) / 2

    anchor_pos = (anchor_x, anchor_y)

    if int(answers["underline_count"]) > 0:
        # Get the bbox of the first n letter to underline
        first_letters_bbox = draw.textbbox(
            anchor_pos,
            answers["name"][: int(answers["underline_count"])],
            font=font,
            anchor=anchor_type,
        )

        # Get the underline position
        underline_start_x = first_letters_bbox[0] - int(answers["additionnal_bar_width"])
        underline_start_y = first_letters_bbox[3] + int(answers["gap"])

        underline_end_x = int(answers["additionnal_bar_width"]) + first_letters_bbox[2]

        underline_end_y = underline_start_y + int(answers["bar_size"])

        underline_start = (underline_start_x, underline_start_y)
        underline_end = (underline_end_x, underline_end_y)

        underline_pos = (underline_start, underline_end)

        # Underline the first letter
        draw.rectangle(underline_pos, fill=accent, width=answers["bar_size"])

    # Draw the text
    draw.text(
        anchor_pos,
        answers["name"],
        font=font,
        fill=text,
        anchor=anchor_type,
    )

    # Redraw the first letter
    draw.text(
        anchor_pos,
        answers["name"][0],
        font=font,
        fill=accent,
        anchor=anchor_type,
    )

    return image
