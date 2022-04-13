import printer
import config
import cmdCommands


def network_startup():
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
                    return temp  # if command ens setup, then temp is equal to netInter object of main network
        if not isCommand:
            # write non-command handler here
            pass


if __name__ == '__main__':
    main_network = network_startup()
    main_network.inputTick()
