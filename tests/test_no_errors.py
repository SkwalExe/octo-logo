import pytest

# The project's venv must be activated, so that
# Octologo is imported directly from src/octologo
from octologo.__main__ import OctoLogoApp


@pytest.mark.asyncio
async def test_no_errors() -> None:
    app = OctoLogoApp()
    async with app.run_test() as pilot:
        await pilot.pause()

        keypress_sequences = [
            # Enter project name
            ("M", "y", "P", "r", "o", "j", "e", "c", "t", "enter"),
            # select default style (just click next)
            ("tab", "tab", "enter"),
            # select default font
            ("tab", "enter"),
            # select default color scheme
            ("tab", "tab", "enter"),
            # default value for the next 6 questions
            ("enter",) * 6,
        ]

        for keys in keypress_sequences:
            await pilot.press(*keys)
            await pilot.pause()

        # The test ends before the image gets generated
