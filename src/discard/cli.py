'''This module contains the entry point for the application.'''

from . import __version__
from . import printer
from . import globals
from . import commands


def network_startup():
    '''
    Lets the user execute commands in a loop until the
    user runs a command with `command.should_finish_startup()`
    equal to `True`.
    '''
    printer.logo()
    print('\n\n')
    print(f'welcome to Discard v{__version__} !')
    printer.random_slogan()
    commands.commands['help'].execute()
    while True:
        cmd = input("<Discard>: ")
        isCommand = False
        for key, command in commands.commands.items():
            if cmd == key:
                isCommand = True
                temp = command.execute()
                if command.should_finish_startup():
                    return temp   # `temp` must be a valid `NetInter`.
        if not isCommand:
            pass


def main():
    '''Entry point for the application.'''
    main_network = network_startup()
    main_network.inputTick()
