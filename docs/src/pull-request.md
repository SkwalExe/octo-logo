# Creating a pull request

If you'd like to contribute, please open an empty pull request and provide an explanation of your proposed changes. Once I approve it, you can begin your work. It's always disheartening to reject a pull request after someone has invested a lot of time and effort into it :(

## Setting up the development environment 🖥️

> Before starting, make sure you have `pdm` installed on your system. You can find the instructions in the [previous page](understanding-the-project#general-info).

1. [Fork this repository to your own GitHub account.](https://github.com/SkwalExe/octo-logo/fork)

2. Clone your fork locally.

```bash
git clone https://github.com/YOUR_USERNAME/octo-logo
cd ./octo-logo
```

3. Install dependencies

```bash
pdm install
```

4. You must configure your IDE to use the project's venv (`./.venv`) or your extensions will fail to resolve the dependencies.

5. If you use a command line editor (like vim), you can activate the venv in your shell session, then start vim.

```bash
# Activating the project's venv (linux)
# This command must be run everytime you open a new shell session.
eval $(pdm venv activate)
vim
```

## Making the pull request 👍 {#making-the-pull-request}

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

- You also have to run tests to check if your changes didn't break anything

```bash
pdm run tests
```

- After that, add your changes to `CHANGELOG.md` and update the README if needed.

- It would also be appreciated if you updated the documentation (`/docs`) according to your changes.

- Do not increment the module version yourself, the maintainer will do it.

- Now, you can commit your work and push to your fork.

```bash
git add --all 
git commit -m "Added a new feature"
git push -u origin my-new-feature
```

- Finally, you can create your pull request from your fork repo's github page.

