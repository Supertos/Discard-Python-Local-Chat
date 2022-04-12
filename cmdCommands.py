import socket
import network_base
import _thread
import random
def cmd_help():
    print("============================")
    print("/help - show this text")
    print("/quit - stop discard'ing")
    print("/host - start server")
    print("/connect - connect to server")
    print("============================")


def cmd_quit():
    quit(0)


def cmd_host():
    global NET_INTERFACE
    NET_INTERFACE = network_base.NetInter()
    NET_INTERFACE.hostMode = True
    NET_INTERFACE.updateGreetings()
    print("============================")
    print("Welcome to server setup wizard!")
    adr = input("*Input hostname (or press enter if unsure): ")
    if adr == "":
        adr = socket.gethostbyname(socket.gethostname())
    NET_INTERFACE.makeSocket( adr, int( input("*Enter desired port: ")) )
    NET_INTERFACE.name = input("*Enter desired name: ")
    print("*Now hosting at "+NET_INTERFACE.address+":"+str(NET_INTERFACE.port))
    _thread.start_new_thread( NET_INTERFACE.serverTick, () )
    _thread.start_new_thread( NET_INTERFACE.inputTick, () )
    while True:
        pass

def cmd_connect():
    global NET_INTERFACE
    NET_INTERFACE = network_base.NetInter()
    print("============================")
    print("Welcome to server setup wizard!")
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
    'connect' : cmd_connect
}