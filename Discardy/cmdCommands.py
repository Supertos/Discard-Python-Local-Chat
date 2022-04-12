def cmd_help():
    print("============================")
    print("/help - show this text")
    print("/quit - stop discard'ing")
    print("/host - start server")
    print("/connect - connect to server")
    print("============================")


def cmd_quit():
    quit(0)


commands = {
    'help' : cmd_help,
    'quit' : cmd_quit
}