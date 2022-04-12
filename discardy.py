import printer
import config
from cmdCommands import commands

def startup():
    #setup_net()
    printer.logo()
    print('\n\n')
    print(f'welcome to Discard v{config.APP_VERSION} !')
    printer.random_slogan()


def main_msg_loop():
    cmd = input("<Discard>: ")
    isCommand = False
    for key, command in commands.items():
        if cmd == key:
            isCommand = True
            command()
    if not isCommand:
        # write non-command handler here
        pass


if __name__ == '__main__':
    startup()
    main_msg_loop()
