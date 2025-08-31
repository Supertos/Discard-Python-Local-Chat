'''
Entry point for discard package.

This module allows executing the package as a module:
> python -m myapp [arguments]

Or if installed as a package:
> myapp [arguments]
'''

from .discardy import main

if __name__ == '__main__':
    main()
