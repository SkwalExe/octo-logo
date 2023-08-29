from . import underline_core

name = "First letter underlined"
active = True

def get_image(name):
    return underline_core.get_image(name, "first_letter")