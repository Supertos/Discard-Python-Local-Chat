import socket
import network_base
import _thread
import random

IPV6 = False
def cmd_help():
    print("============================")
    print("help - show this text")
    print("quit - stop discard'ing")
    print("host - start server")
    print("connect - connect to server")
    print("ipv6 - changes to ipv6 mode")
    print("============================")


def cmd_quit():
    quit(0)


def cmd_host():
    global NET_INTERFACE
    global IPV6
    NET_INTERFACE = network_base.NetInter()
    NET_INTERFACE.ipv6 = IPV6
    NET_INTERFACE.hostMode = True
    NET_INTERFACE.updateGreetings()
    print("============================")
    print("Welcome to server setup wizard!")
    adr = input("*Input hostname (or press enter if unsure): ")
    if adr == "":
        if IPV6:
            adr = socket.getaddrinfo(socket.gethostname(), 8080, socket.AF_INET6)[0][4][0]
        else:
            adr = socket.gethostbyname(socket.gethostname())
    if not IPV6:
        NET_INTERFACE.makeSocket( adr, int( input("*Enter desired port: ")) )
    else:
        NET_INTERFACE.makeSocket(adr, 8080)
    NET_INTERFACE.name = input("*Enter desired name: ")
    print("*Now hosting at "+NET_INTERFACE.address+":"+str(NET_INTERFACE.port))
    _thread.start_new_thread( NET_INTERFACE.serverTick, () )
    _thread.start_new_thread( NET_INTERFACE.inputTick, () )
    while True:
        pass

def cmd_ipv6():
    global IPV6
    IPV6 = not IPV6
    if IPV6:
        print("Now using IPv6!")
    else:
        print("Now using IPv4!")
def cmd_connect():
    global NET_INTERFACE
    global IPV6
    NET_INTERFACE = network_base.NetInter()
    print("============================")
    print("Welcome to server setup wizard!")
    NET_INTERFACE.ipv6 = IPV6
    if IPV6:
        NET_INTERFACE.makeSocket(socket.getaddrinfo(socket.gethostname(), 8080, socket.AF_INET6)[0][4][0], 8080)
    else:
        NET_INTERFACE.makeSocket( socket.gethostbyname(socket.gethostname()), random.randint(1000, 9999) )
    NET_INTERFACE.name = input("*Enter desired name: ")
    adr = input("*Enter desired address: ")
    NET_INTERFACE.connect( adr.split(":")[0], int(adr.split(":")[1]))
    _thread.start_new_thread( NET_INTERFACE.clientTick, () )
    _thread.start_new_thread( NET_INTERFACE.inputTick, () )
    while True:
        pass
commands = {
    'help' : cmd_help,
    'quit' : cmd_quit,
    'host' : cmd_host,
    'connect' : cmd_connect,
    'ipv6' : cmd_ipv6
}