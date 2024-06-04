from collections.abc import Generator
from typing import Any

import inquirer as inq
from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Input, Label, Select, Static

from octologo.utils import logger

# from textual import log


class QuestionBase:
    name: str
    label: str

    def __init__(self, name: str, label: str) -> None:
        self.name = name
        self.label = label


class TextQuestion(QuestionBase):
    validators: list[Validator] | None
    placeholder: str
    default_value: str

    def __init__(
        self,
        name: str,
        label: str,
        validators: list[Validator] | None = None,
        placeholder: str = "",
        default_value: str = "",
    ) -> None:
        super().__init__(name, label)
        self.validators = validators
        self.placeholder = placeholder
        self.default_value = default_value

    def as_widget(self) -> Input:
        """Returns a Textual input widget with the correcponding information"""
        _input = Input(
            classes="full-width",
            id=self.name,
            placeholder=self.placeholder,
            validators=self.validators,
        )
        _input.border_title = self.label
        _input.value = self.default_value
        return _input


class SelectQuestion(QuestionBase):
    options: list[tuple[str, Any]]
    default_value: Any | None = None

    def __init__(self, name: str, label: str, options: list[tuple[str, Any]], default_value: str | None = None) -> None:
        super().__init__(name, label)
        self.options = options
        self.default_value = default_value

    def as_widget(self) -> Select:
        _select = Select(
            classes="full-width",
            id=self.name,
            options=self.options,
            allow_blank=False,
            value=self.default_value,
        )

        _select.border_title = self.label

        return _select


class BackNextButtons(Static):
    def compose(self) -> Generator:
        yield Button("Back", variant="warning", id="back")
        yield Button("Next", variant="success", id="next")


class Wizard(Static):
    question_index = reactive(-1)
    answers: dict = dict()
    selected_question: None | Select | Input = None
    questions: list[SelectQuestion | TextQuestion]
    input_message: Label
    title: str = "Wizard"

    # The message sent when the "next" button is clicked while on the last question
    class Finished(Message):
        answers: dict
        wizard_id: str | None

        def __init__(self, answers: dict, wizard_id: str | None) -> None:
            self.answers = answers
            self.wizard_id = wizard_id
            super().__init__()

    @on(Button.Pressed, "#back")
    def on_back(self) -> None:
        # When the back button is pressed, just go to the previous question
        # It cannot be pressed if there arent any questions before
        self.question_index -= 1

    @on(Button.Pressed, "#next")
    async def on_next(self) -> None:
        # If the selected question is an input then fire the submit event so that
        # validation is made and the next question is shown.
        # Else, just go to the next question since a select cannot be invalid
        if isinstance(self.selected_question, Input):
            await self.selected_question.action_submit()
        else:
            self.question_index += 1

    def handle_validation_result(self, validation_result: ValidationResult | None) -> None:
        if self.selected_question is None:
            raise Exception("selected_question should not be None")

        if validation_result is None or validation_result.is_valid:
            # If the validation is OK then hide the error message and set the input color back to normal
            # Also, reenable the next button
            self.query_one("#next").disabled = False
            self.selected_question.remove_class("invalid")
            self.input_message.add_class("hidden")

        else:
            # If the validation comports an error then disable the next button,
            # Show and set the content of the error message and set the input's color to red
            self.query_one("#next").disabled = True
            self.input_message.remove_class("hidden")
            self.input_message.renderable = validation_result.failure_descriptions[0]
            self.selected_question.add_class("invalid")

    def on_input_changed(self, message: Input.Changed) -> None:
        # When an input is changed, save its new value into the self.answers dict
        self.answers[message.input.id] = message.value

        # Show error messages if any
        self.handle_validation_result(message.validation_result)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        # Handle the validation result to show
        # a message if there are any errors
        self.handle_validation_result(message.validation_result)

        # When the input is submitted, if it is valid then go to the next question
        if message.validation_result is None or message.validation_result.is_valid:
            self.question_index += 1

    def on_select_changed(self, message: Select.Changed) -> None:
        # When a select is changed update the value in the self.answers dict
        self.answers[message.select.id] = message.value

    def compose(self) -> Generator:
        # Render directly every input
        # They are all hidden by default
        for i, question in enumerate(self.questions):
            wid = question.as_widget()

            # For every select, the value in the answers dict
            # will not be updated if the user just keeps the default value
            # and click next without changing the value,
            # the on_select_changed function will not be called and the
            # answers dict will not contain the key corresponding to the select which can result in a KeyError
            if isinstance(wid, Select):
                self.answers[wid.id] = question.default_value

            # Hide every questions except the first one
            if i != 0:
                wid.add_class("hidden")

            # mount the question
            yield wid

        # The error message below inputs if there are any errors
        self.input_message = Label("This is the input error message", id="input_message", classes="hidden")
        self.input_message.styles.color = "tomato"
        self.input_message.styles.max_width = "100%"
        yield self.input_message

        # ----------------------------
        yield BackNextButtons()

    def on_mount(self) -> None:
        # Trigger the watch_question_index function to make the first input appear
        self.question_index = 0

    def watch_question_index(self) -> None:
        """Called when the question index changes"""

        # Add 'hidden' class to the previous shown input if any
        if self.selected_question is not None:
            self.selected_question.add_class("hidden")

        # If the question index has been incremented but it is now out of bound then
        # the user clicked next on the last question
        if self.question_index >= len(self.questions):
            self.post_message(self.Finished(self.answers, self.id))
            return

        # Put the question index in the border title
        self.border_title = f"{self.title} [{self.question_index + 1}/{len(self.questions)}]"

        # Show the input corresponding to the new value of self.question_index
        element = self.query_one(f"#{self.questions[self.question_index].name}")
        if not isinstance(element, (Input, Select)):
            raise Exception("Wanted Input or Select but got something else")
        self.selected_question = element
        self.selected_question.remove_class("hidden")
        self.selected_question.focus()

        # If the first question has just been selected then disable
        # the "Back" button since there arent any questions before
        self.query_one("#back").disabled = self.question_index == 0


def validate_text_question(question: TextQuestion, value: str) -> bool:
    if question.validators is None:
        return True

    for validator in question.validators:
        validation = validator.validate(value)
        if not validation.is_valid:
            logger.error(validation.failure_descriptions[0])
            return False

    return True


def inq_ask(questions: list[SelectQuestion | TextQuestion]) -> dict[str, Any]:
    answers = dict()

    for question in questions:
        if isinstance(question, SelectQuestion):
            answers[question.name] = inq.list_input(
                question.label, choices=question.options, default=question.default_value
            )

        elif isinstance(question, TextQuestion):
            while True:
                temp = inq.text(question.label, default=question.default_value)
                if not validate_text_question(question, temp):
                    continue

                answers[question.name] = temp
                break

    return answers
