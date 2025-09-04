# Discard

> This project is dedicated to creating new and independant Russian messanger Discard!!!
> 
> — God, before creating the space and time.

This app is a simple command line chat over a local network.

## Overview

Discard is a command line app that allows you to exchange quirky text messages
with other Discard users over a local network.

This app is implemented in pure python and does not need any external package
dependencies (except for the build tools, but they are only used by the developers).

## Usage

Discard is used from the command line. 

```bash
# prints versision information
discard version
```

For a complete list of commands run:

```bash
discard --help
```

## Build (for developers)

To build the python package:
```bash
pip install setuptools
pip install . -e  # "-e" allows to edit the source without rebuilding, see pip docs.
```

To build the standalone executable:
```bash
pip install pyinstaller
pyinstaller ./src/discard.py --onefile
```
