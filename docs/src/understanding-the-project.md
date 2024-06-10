# Understanding the Project's Structure

## General Info About the Project 📖 {#general-info}

This is a terminal application that allows developers to generate logos (maybe a better term would be banner) for their projects. It uses the following technologies for the development process and for the build pipeline:

- [PDM](https://pdm-project.org/en/latest/) for development scripts and managing (dev)dependencies.
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [Pyright](https://microsoft.github.io/pyright/#/) for type checking
- [Pytest](https://docs.pytest.org/) for unit tests

You can install PDM with the following command:

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

The project also uses [`Vitepress`](https://vitepress.dev/) for generating the [documentation website](https://octologo.skwal.net).

## Files and directories 📂 {#files-and-directories}

__Configuration Files:__ ⚙

- `ruff.toml`: Ruff configuration file (for linting and formatting)
- `pyproject.toml`: Python module configuration

__Source:__ 🔢
- `src/octologo/colors/`: Contains color schemes (.toml files).
- `src/octologo/fonts/`: Contains font files that can be used in the app.
- `src/octologo/styles/`: Contains available logo styles.
- `src/octologo/__main__.py`: Application entry point.

__Other:__ 📄

- `assets/`: Assets for the GitHub repo only.
- `tests/`: Unit test files (pytest).
- `docs/`: Documentation site (Vitepress)

## PDM scripts

- `format`: Checks for formatting errors and fixes them if possible.
- `format-check`: Checks for formatting errors and exists with error code if any is found.
- `lint`: Checks for linting errors and fixes them if possible.
- `lint-check`: Check for linting errors and exits with error code if any is found.
- `check-types`: Check for type errors with Pyright.
- `tests`: Run all unit tests.
