# Group 11

## Quick Start Guide

### Setting up the Environment

This project uses Poetry for version control, see [poetry documentation](https://python-poetry.org/docs/cli/) for more detail. If you don't have poetry installed in your environment, run

```plaintext
pip install poetry
```

A list of packages necessary to run the project is contained in the poetry.lock file.

To add packages to the .toml file (you should never touch the .lock file directly) use:

```plaintext
poetry add <package_name>
```

To remove packages use: 

```plaintext
poetry remove <package_name>
```

To install all the packages in the .lock file use the command:

```plaintext
poetry install
```

Before running any scripts, you will need to enter your poetry environment by typing:

```plaintext
poetry shell
```
