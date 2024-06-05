<p align="center">
  <img src="https://raw.githubusercontent.com/SkwalExe/octo-logo/main/assets/logo.png">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/SkwalExe/octo-logo?style=for-the-badge">
  <img src="https://img.shields.io/github/stars/SkwalExe/octo-logo?style=for-the-badge">
  <img src="https://img.shields.io/github/issues/SkwalExe/octo-logo?color=blueviolet&style=for-the-badge">
  <img src="https://img.shields.io/github/forks/SkwalExe/octo-logo?color=teal&style=for-the-badge">
  <img src="https://img.shields.io/github/issues-pr/SkwalExe/octo-logo?color=tomato&style=for-the-badge">

</p>

<p align="center">💠 Simple program that generates a logo for your open source projects 💠</p>

# Credits

I had the idea to create this project after seeing the logos made by [adi1090x](https://github.com/adi1090x) for his repositories. They were simple but gave a nice feel to his projects. I wanted a logo that gives the same energy, but didn't manage to find how he made them (most likely manually, with GIMP according the the exif data of the images). So I decided to make a program that would allow anyone to generate a cool and simple logo for their projects.

- [adi1090x's GitHub](https://github.com/adi1090x)

# How to install 📥

You can install octologo easily with pip:

```bash
python3 -m pip install octologo
```

You can also use [pipx](https://pypa.github.io/pipx/):

```bash
pipx install octologo
```

Now, start the app with:

```bash
octologo
```

> [!CAUTION]
> If the command is not found after installtion, you must add  `~/.local/bin` to your path. You can do this by adding `export PATH=$PATH:~/.local/bin` to your `.bashrc` or `.zshrc` file.

```bash
# For bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc

# For zsh
echo 'export PATH=$PATH:~/.local/bin' >> ~/.zshrc
```

# Styles

### Style 1 - First letters underlined

> The number of letters to underline is customizable since version 2.0.0

<p align="center">
  <img src="https://raw.githubusercontent.com/SkwalExe/octo-logo/main/assets/style1.png">
</p>


# Color schemes

### Color scheme 1 - adi1090x's color scheme

<p align="center">
  <img src="https://raw.githubusercontent.com/SkwalExe/octo-logo/main/assets/color1.png">
</p>

### Color scheme 2 - Cherry

<p align="center">
  <img src="https://raw.githubusercontent.com/SkwalExe/octo-logo/main/assets/color2.png">
</p>

### Color scheme 3 - Midnight Abyss

<p align="center">
  <img src="https://raw.githubusercontent.com/SkwalExe/octo-logo/main/assets/color3.png">
</p>

# Contributing 🤝

Please, open an issue if you have any suggestion or if you found a bug. I will try to fix it as soon as possible.

## General Info About the Project 📖

This is a terminal application that allows developers to generate logos for their projects. It uses the following technologies for the development process and for the build pipeline:

- [PDM](https://pdm-project.org/en/latest/) for development scripts and managing (dev)dependencies.
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [Pyright](https://microsoft.github.io/pyright/#/) for type checking

You can install PDM with the following command:

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

## Setting up the development environment 🖥️

- [Fork this repository to your own GitHub account.](https://github.com/SkwalExe/octo-logo/fork)

- Clone your fork locally.

```bash
git clone https://github.com/YOUR_USERNAME/octo-logo
cd ./octo-logo
```

- Install dependencies

```bash
pdm install
```

## Files and directories 📂

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

## Creating a pull request 👍

If you'd like to contribute, please open an empty pull request and provide an explanation of your proposed changes. Once I approve it, you can begin your work. It's always disheartening to reject a pull request after someone has invested a lot of time and effort into it. 😿

- Create a branch for your contribution

```bash
git checkout -b my-new-feature
```

- When you finished your changes, you must check your code's formatting and linting and fix all the errors.

```bash
pdm run format # Check for formatting errors (most errors should be automatically fixed)
pdm run lint # Check for linting errors
pdm run check-types # Check for type errors
```

- After that, add your changes to `CHANGELOG.md` and update the README if needed.

- Do not increment the module version yourself, the maintainer will do it.

- Then, you can commit your work and push to your fork.

```bash
git add --all 
git commit -m "Added a new feature"
git push -u origin my-new-feature
```

- Finally, you can create your pull request from your fork repo's github page.

## PDM scripts

- `format`: Checks for formatting errors and fixes them if possible.
- `format-check`: Checks for formatting errors and exists with error code if any is found.
- `lint`: Checks for linting errors and fixes them if possible.
- `lint-check`: Check for linting errors and exits with error code if any is found.
- `check-types`: Check for type errors with Pyright.
