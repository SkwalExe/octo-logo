import inquirer as inq
from importlib import import_module
import os
from time import time
from utils import *

# Look for DEBUG in the environment variables
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

def main():

    # Load the styles in the styles directory
    styles = dict()
    for style in os.listdir(os.path.join(BASE_DIR, "src", "styles")):
        # Only keep .py files
        if not style.endswith(".py"):
            continue

        # Try to import the script
        # If it fails, ignore it
        if DEBUG:
            module = import_module(f"styles.{remove_ext(style)}")
        else:
            try:
                module = import_module(f"styles.{remove_ext(style)}")
            except:
                print(f"Error while importing {style}, ignoring...")
                continue

        # Only keep files with the active attribute set to True
        # This allows to ignore some scripts that may be in the styles directory
        if not module.active:
            continue

        styles[module.name] = module

    questions = [
        inq.Text("name", message="Project's name"),
        inq.List("style", message="Select a style", choices=list(styles.keys()))
    ]

    answers = inq.prompt(questions)

    # Force the user to enter a name
    if not len(answers["name"]) > 0:
        print("Error : You must enter a name")
        quit()

    selected_style = styles[answers["style"]]

    image = selected_style.get_image(answers["name"])

    # Save result or show if debug is enabled
    save_to = f'output/{answers["name"]}_{int(time())}.png'
    image.show() if DEBUG else image.save(save_to)
    print(f"Logo saved to {save_to}")

if __name__ == "__main__":
    main()
