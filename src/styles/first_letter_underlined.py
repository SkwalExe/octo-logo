from . import underline_core

display_name = "First letter underlined"
active = True
questions = underline_core.questions

def get_image(answers):
    return underline_core.get_image(answers, "first_letter")