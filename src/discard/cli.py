'''This module contains the entry point for the application.'''

from . import __version__
from . import commands


def main():
    '''Entry point for the application.'''
    command_loop()


def command_loop():
    '''
    Lets the user execute commands in a loop until one of the
    commands quits the application.
    '''
    start_message()
    commands.commands.try_execute('help')
    while True:
        name = input('<Discard>: ')
        if not commands.commands.try_execute(name):
            print(f'No such command: {name}')


def start_message():
    '''
    Prints the startup message for when the
    application begins its execution.
    '''
    print('              ######                ####        #####       ##      ########        ######      ')
    print('            ####   ###       # #  ###   ##    ####   ###   #  #     #       #      #####        ')
    print('         #######     ####   # ##  ##         ##           ##  ##    #   ##   #     ###      #   ')
    print('             ###      ####         ######   ###          ##    ##   #        #     ##      ##   ')
    print('        ########    ####   ####         ##   ##          ########   #   # #  #     #      ###   ')
    print('     ###########   ###    ####    ##   ###    ####   ###  ##  ##    #   #  #  #        #####    ')
    print('           #########     #####      ####        #####    ##    ##   #####   ####   #######      ')
    print('\n\n')
    print(f'welcome to Discard v{__version__} !')
    random_slogan()


def random_slogan():
    '''Prints a randomly chosen slogan out of a predefined list.'''
    from random import choice
    slogans = [
        'now without Discard!',
        'discard',
        'why??',
        '...',
        'press alt + F4 for help'
    ]
    print(f'\t{choice(slogans)}')
