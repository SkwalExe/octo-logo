# ---------------------------------------- Standard Imports
import os
from collections.abc import Generator

# ---------------------------------------- External Imports
from click_extra import ExtraContext, Parameter, extra_command, option
from PIL.Image import Image
from textual.app import App
from textual.events import Key
from textual.validation import Length
from textual.widgets import Footer, Header, Label, LoadingIndicator

# ---------------------------------------- Local Imports
from octologo import __version__
from octologo.utils import BASE_DIR, get_output_filename, logger, style_names, styles
from octologo.wizard import SelectQuestion, TextQuestion, Wizard, inq_ask

BASIC_INFO_QUESTIONS = [
    TextQuestion(
        "name",
        "Your project's name",
        [Length(1, failure_description="Your project's name cannot be blank")],
        "super-octo-project",
    ),
    SelectQuestion("style", "Logo Style", style_names, "first_letter_underlined"),
]


class OctoLogoApp(App):
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+t", "toggle_dark", "Toggle Dark Mode"),
    ]
    answers = dict()

    CSS_PATH = os.path.join(BASE_DIR, "app.tcss")
    TITLE = "Octo Logo Wizard"
    finished: bool = False
    result: Image | None = None
    loading_wid: LoadingIndicator = LoadingIndicator(classes="hidden")

    async def on_key(self, event: Key) -> None:
        if event.key == "enter" and self.finished:
            await self.action_quit()
        elif event.key == "v" and self.finished:
            if self.result is None:
                raise Exception("self.result should not be null")
            self.result.show()

    def on_wizard_finished(self, message: Wizard.Finished) -> None:
        # Get the wizard answers and the wizard's id
        self.answers.update(message.answers)
        finished_wizard_id = message.wizard_id

        # remove the wizard
        self.query_one(f"#{finished_wizard_id}").remove()

        # When the basic info wizard is finished, mount the style-specific wizard
        if finished_wizard_id == "basic_info_wizard":
            style_wizard = Wizard(id="style_wizard")
            style_wizard.questions = styles[self.answers["style"]].module.questions
            style_wizard.title = "Style Settings"
            self.mount(style_wizard)
        # When the style-specific wizard is finished, create the image and save it
        elif finished_wizard_id == "style_wizard":
            style = styles[self.answers["style"]].module
            self.result = style.get_image(self.answers)
            self.loading_wid.remove_class("hidden")
            self.set_timer(2, self.final_message)

    # Final message
    def final_message(self) -> None:
        if self.result is None:
            raise Exception("self.result should not be none in OctoLogoApp.final_message")

        save_to = get_output_filename(self.answers["name"])

        self.loading_wid.add_class("hidden")
        self.mount(
            Label(
                f"Logo saved to [bold]{save_to}[/bold].\n"
                f"[blue blink]-> Press v to view the result[/blue blink]\n"
                f"[red]Press enter to quit[/red]"
            )
        )
        self.result.save(save_to)
        self.finished = True

    def compose(self) -> Generator:
        self.app.title = f"Octo Logo v{__version__}"

        yield Header(show_clock=True)
        yield Footer()

        basic_info_wizard = Wizard(id="basic_info_wizard")
        basic_info_wizard.questions = BASIC_INFO_QUESTIONS
        basic_info_wizard.title = "Basic Information"
        yield basic_info_wizard
        yield self.loading_wid


def disable_ansi(ctx: ExtraContext, _: Parameter, val: bool) -> bool:
    ctx.color = not val

    # We must return the value for the main function no_ansi parameter not to be None
    return val


@extra_command(params=[])
@option("-t", "--no-tui", is_flag=True, help="Dont use the Textual Terminal User Interface")
def main(no_tui: bool) -> None:
    if no_tui:
        # If the tui is disabled, do everything without textual
        answers = dict()

        answers.update(inq_ask(BASIC_INFO_QUESTIONS))
        answers.update(inq_ask(styles[answers["style"]].module.questions))

        style = styles[answers["style"]].module
        result = style.get_image(answers)

        save_to = get_output_filename(answers["name"])
        result.save(save_to)
        logger.success(f"Image saved to : {save_to}")
    else:
        # If the tui is enabled, run the textual app
        app = OctoLogoApp()
        app.run()
        quit(0)
