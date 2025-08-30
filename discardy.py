'''This module is the entry point for the application.'''

import printer
import config
import cmdCommands


def network_startup():
    '''
    Lets the user execute commands in a loop until the
    user runs a command with `command.should_finish_startup()`
    equal to `True`.
    '''
    printer.logo()
    print('\n\n')
    print(f'welcome to Discard v{config.APP_VERSION} !')
    printer.random_slogan()
    cmdCommands.commands['help'].execute()
    while True:
        cmd = input("<Discard>: ")
        isCommand = False
        for key, command in cmdCommands.commands.items():
            if cmd == key:
                isCommand = True
                temp = command.execute()
                if command.should_finish_startup():
                    return temp   # `temp` must be a valid `NetInter`.
        if not isCommand:
            pass


if __name__ == '__main__':
    main_network = network_startup()
    main_network.inputTick()
