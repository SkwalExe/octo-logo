from . import underline_core

name = "All text underlined"
active = True

def get_image(name):
    return underline_core.get_image(name, "all")