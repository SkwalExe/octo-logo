![Project's logo](./logo.png)

<p align="center">💠 Simple logos for complex projects 💠</p>

## Credits 

I had the idea to create this project after seeing the logos made by [adi1090x](https://github.com/adi1090x) for his repositories. They were simple but gave a nice feel to his projects. I wanted a logo that gives the same energy, but didn't manage to find how he made them (most likely manually, with GIMP according the the exif data of the images). So I decided to make a program that would allow anyone to generate cool and simple logos for their projects.

## Installation 📥 {#installation}

OctoLogo requires Python version 3.9 or higher.

::: warning Command not found

If the command is not found after installation, it may be because the `~/.local/bin` directory is not in your path. You can fix this probem by adding `export PATH=$PATH:~/.local/bin` to your `.bashrc` or `.zshrc` file.

```bash
# For bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc

# For zsh
echo 'export PATH=$PATH:~/.local/bin' >> ~/.zshrc
```
:::


### Via pipx (recommended)

```bash
pipx install octologo
```

### Via pip

```bash
pip install octologo
```

---

**🎉 You can now use the app with the `octologo` command!**
