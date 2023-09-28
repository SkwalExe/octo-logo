import os
from time import time
from utils import *

from textual.app import App
from textual.widgets import Header, Footer, Label, LoadingIndicator
from textual.validation import Length
from textual import log
from textual.events import Key

VERSION = "1.0.0"

from wizard import *

class OctoLogoApp(App):
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+t", "toggle_dark", "Toggle Dark Mode")
    ]
    answers = dict()

    CSS_PATH = os.path.join(BASE_DIR, "src", "app.tcss")
    TITLE = "Octo Logo Wizard"
    finished: bool = False
    save_to: str | None = None
    result: Image.Image | None = None
    loading_wid: LoadingIndicator = LoadingIndicator(classes="hidden")

    async def on_key(self, event: Key):
        if event.key == "enter" and self.finished:
            await self.action_quit()
        elif event.key == "v" and self.finished:
            self.result.show()


    def on_wizard_finished(self, message: Wizard.Finished):
        # Get the wizard answers and the wizard's id
        self.answers.update(message.answers)
        finished_wizard_id = message.wizard_id

        # remove the wizard
        self.query_one(f"#{finished_wizard_id}").remove()

        # When the basic info wizard is finished, mount the style-specific wizard
        if finished_wizard_id == "basic_info_wizard":
            style_wizard = Wizard(id="style_wizard")
            style_wizard.questions = styles[self.answers['style']].module.questions
            style_wizard.title = "Style Settings"
            self.mount(style_wizard)
        # When the style-specific wizard is finished, create the image and save it 
        elif finished_wizard_id == "style_wizard":
            style = styles[self.answers['style']].module
            self.result = style.get_image(self.answers)
            self.save_to = f'output/{self.answers["name"]}_{int(time())}.png'
            self.loading_wid.remove_class("hidden")
            self.set_timer(2, self.final_message)

    # Final message
    def final_message(self):
        self.loading_wid.add_class("hidden")
        self.mount(Label(f"Logo saved to [bold]{self.save_to}[/bold].\n[blue blink]-> Press v to view the result[/blue blink]\n[red]Press enter to quit[/red]"))
        self.result.save(self.save_to)
        self.finished = True
            

    def compose(self):
        self.app.title = f"Octo Logo v{VERSION}"

        yield Header(show_clock=True)
        yield Footer()

        basic_info_wizard = Wizard(id="basic_info_wizard")
        basic_info_wizard.questions = [
            TextQuestion("name", "Your project's name", [Length(1,  failure_description="Your project's name cannot be blank")], "super-octo-project" ),
            SelectQuestion("style", "Logo Style", style_names, "first_letter_underlined")
        ]
        basic_info_wizard.title = "Basic Information"
        yield basic_info_wizard
        yield self.loading_wid

def main():

    app = OctoLogoApp()
    app.run()
    quit(0)

if __name__ == "__main__":
    main()
