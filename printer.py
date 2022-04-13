from random import randint
def random_slogan():
    slogans = [
        'now without Discard!',
        'discard',
        'why??',
        '...',
        'press alt + F4 for help'
    ]
    print(f'\t{slogans[randint(0, len(slogans) - 1)]}')


def logo():
    print('              ######                ####        #####       ##      ########        ######      ')
    print('            ####   ###       # #  ###   ##    ####   ###   #  #     #       #      #####        ')
    print('         #######     ####   # ##  ##         ##           ##  ##    #   ##   #     ###      #   ')
    print('             ###      ####         ######   ###          ##    ##   #        #     ##      ##   ')
    print('        ########    ####   ####         ##   ##          ########   #   # #  #     #      ###   ')
    print('     ###########   ###    ####    ##   ###    ####   ###  ##  ##    #   #  #  #        #####    ')
    print('           #########     #####      ####        #####    ##    ##   #####   ####   #######      ')