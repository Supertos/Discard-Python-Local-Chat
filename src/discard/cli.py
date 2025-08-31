'''This module contains the entry point for the application.'''

from . import __version__
from . import printer
from . import globals
from . import commands


def command_loop():
    '''
    Lets the user execute commands in a loop until one of the
    commands quits the application.
    '''
    printer.logo()
    print('\n\n')
    print(f'welcome to Discard v{__version__} !')
    printer.random_slogan()
    commands.commands.try_execute('help')
    while True:
        name = input('<Discard>: ')
        if not commands.commands.try_execute(name):
            print(f'No such command: {name}')


def main():
    '''Entry point for the application.'''
    command_loop()
