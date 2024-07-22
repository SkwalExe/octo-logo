from click_extra import extra_command, option
from textual_wizard import Wizard
from textual_wizard.inputs import Select, Text

from octologo import __version__
from octologo.utils import get_output_filename, logger, style_names, styles

BASIC_INFO_QUESTIONS = [
    Text(
        "name",
        "Your project's name",
        placeholder="super-octo-project",
    ),
    Select("style", "Logo Style", options=style_names, default_value="first_letter_underlined"),
]


def handle_wizard_cancelled() -> None:
    logger.error("Wizard cancelled by user.")
    quit(0)


@extra_command(params=[])
@option("-t", "--no-tui", is_flag=True, help="Dont use the Textual Terminal User Interface")
def main(no_tui: bool) -> None:
    app_title = f"Octologo v{__version__}"
    wiz1 = Wizard(BASIC_INFO_QUESTIONS, app_title, "Basic Information", disable_tui=no_tui)
    answers = wiz1.run()

    if answers is None:
        handle_wizard_cancelled()
        return

    style = styles[answers["style"]].module
    wiz2 = Wizard(style.questions, app_title, "Specific Information", disable_tui=no_tui)
    res2 = wiz2.run()
    if res2 is None:
        handle_wizard_cancelled()
        return

    answers.update(res2)

    result_image = style.get_image(answers)

    save_to = get_output_filename(answers["name"])
    result_image.save(save_to)
    logger.success(f"Image saved to : {save_to}")
