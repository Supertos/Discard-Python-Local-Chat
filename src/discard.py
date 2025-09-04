'''
This is a bootstrap module to be able to use the `discard` package
when building an `.exe` with pyinstaller.

To build the `.exe`:
```bash
pip install pyinstaller
pyinstaller ./src/discard.py --onefile
```
'''

import discard.cli

if __name__ == '__main__':
    discard.cli.main()
