# Installation Guide

## Interactive Mode (Recommended)

The interactive mode uses arrow keys and provides a polished user experience.

### Install Dependencies

```bash
cd automation
pip3 install -r requirements.txt
```

This installs `questionary` - a lightweight terminal UI library.

### Run

```bash
python3 shop_interactive.py
```

## Command Line Mode (No Installation)

The command line mode requires **zero dependencies** - just pure Python 3!

```bash
python3 recipe_to_shopping_urls.py ../recipes/baking/banana-bread.md
```

## Troubleshooting

### "questionary not found"

If you see an error about questionary missing:

```bash
pip3 install questionary
```

Or use the requirements file:

```bash
pip3 install -r requirements.txt
```

### Permission denied

If pip fails due to permissions, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
python3 shop_interactive.py
```

### Python version

Requires Python 3.7 or higher. Check your version:

```bash
python3 --version
```

## What Gets Installed

- **questionary** (~50KB) - Terminal UI library for arrow key navigation

That's it! Super lightweight.

