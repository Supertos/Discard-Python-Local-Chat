import socket
import network_base
import _thread
import random
import config


def cmd_help():
    print("============================")
    print("help - show this text")
    print("quit - stop discard'ing")
    print("host - start server")
    print("connect - connect to server")
    print("ipv6 - use ipv6 mode")
    print("ipv4 - use ipv4 mode")
    print("============================")


def cmd_quit():
    quit(0)


def cmd_host():
    NET_INTERFACE = network_base.NetInter()
    NET_INTERFACE.ipv6 = config.usingIpv6
    NET_INTERFACE.hostMode = True
    NET_INTERFACE.updateGreetings()
    print("============================")
    print("Welcome to server setup wizard!")
    #adr = input("*Input socket hostname (press enter if unsure): ")
    port = int( input("*Enter desired port: ") )
    #if adr == "":
    if config.usingIpv6:
        adr = socket.getaddrinfo(socket.gethostname(), port, socket.AF_INET6)[0][4][0]
    else:
        adr = socket.gethostbyname(socket.gethostname())
    NET_INTERFACE.makeSocket(adr, port)
    NET_INTERFACE.name = input("*Enter desired name: ")
    print("*Now hosting at "+NET_INTERFACE.address+":"+str(NET_INTERFACE.port))
    _thread.start_new_thread( NET_INTERFACE.serverTick, () )
    return NET_INTERFACE


def cmd_ipv6():
    config.usingIpv6 = True
    print("Now using IPv6!")


def cmd_ipv4():
    config.usingIpv6 = False
    print("Now using IPv4!")



def cmd_connect():
    NET_INTERFACE = network_base.NetInter()
    print("============================")
    print("Welcome to server setup wizard!")
    NET_INTERFACE.ipv6 = config.usingIpv6
    if config.usingIpv6:
        NET_INTERFACE.makeSocket(socket.getaddrinfo(socket.gethostname(), 8080, socket.AF_INET6)[0][4][0], random.randint(1000, 9999) )
    else:
        NET_INTERFACE.makeSocket( socket.gethostbyname(socket.gethostname()), random.randint(1000, 9999) )
    NET_INTERFACE.name = input("*Enter desired name: ")
    adr = input("*Enter desired address: ")
    if config.usingIpv6:
        print(adr[0:(len(adr)-5)],adr[(len(adr)-4):len(adr)])
        NET_INTERFACE.connect(adr[0:(len(adr)-5)], int( adr[(len(adr)-4):len(adr)] ) )
    else:
        NET_INTERFACE.connect(adr.split(":")[0], int(adr.split(":")[1]))
    _thread.start_new_thread( NET_INTERFACE.clientTick, () )
    return NET_INTERFACE


class CmdCommand:
    def __init__(self, __execute, __end_startup):
        self.__end_startup = __end_startup
        self.__execute = __execute  # if startup should end after execution

    def should_finish_startup(self):
        return self.__end_startup

    def execute(self):
        return self.__execute()


commands = {
    'help' : CmdCommand(cmd_help, False),
    'quit' : CmdCommand(cmd_quit, True),
    'host' : CmdCommand(cmd_host, True),
    'connect' : CmdCommand(cmd_connect, True),
    'ipv6' : CmdCommand(cmd_ipv6, False),
    'ipv4' : CmdCommand(cmd_ipv4, False)
}