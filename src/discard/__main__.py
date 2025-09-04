'''
Entry point for discard package.

This module allows executing the package as a module:
> python -m discard [arguments]

Or if installed as a package:
> discard [arguments]
'''

from .cli import main

if __name__ == '__main__':
    main()
