from PIL.Image import Image

from . import underline_core

display_name = "First letters underlined"
active = True
questions = underline_core.questions


def get_image(answers: dict) -> Image:
    return underline_core.get_image(answers)
