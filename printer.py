'''This module contains functions that print text messages.'''

from random import randint
def random_slogan():
    '''Prints a randomly chosen slogan out of a predefined list.'''
    slogans = [
        'now without Discard!',
        'discard',
        'why??',
        '...',
        'press alt + F4 for help'
    ]
    print(f'\t{slogans[randint(0, len(slogans) - 1)]}')


def logo():
    '''Prints the ASCII logo of the application.'''
    print('              ######                ####        #####       ##      ########        ######      ')
    print('            ####   ###       # #  ###   ##    ####   ###   #  #     #       #      #####        ')
    print('         #######     ####   # ##  ##         ##           ##  ##    #   ##   #     ###      #   ')
    print('             ###      ####         ######   ###          ##    ##   #        #     ##      ##   ')
    print('        ########    ####   ####         ##   ##          ########   #   # #  #     #      ###   ')
    print('     ###########   ###    ####    ##   ###    ####   ###  ##  ##    #   #  #  #        #####    ')
    print('           #########     #####      ####        #####    ##    ##   #####   ####   #######      ')