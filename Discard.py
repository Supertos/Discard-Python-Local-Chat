"""-------------------------------------------------
    Discard
    --------------------
    Year: 2022
    Author: Supertos
    Notes:
        Send messages like a boss
-------------------------------------------------"""

import network_base
import random
import os
import socket
import _thread
GLOBAL_ENCODER = network_base.msg_encoder()
GLOBAL_NETWORK = network_base.network_interface()

GLOBAL_ENCODER.bind_interface( GLOBAL_NETWORK )

GLOBAL_HOST = False
GLOBAL_VER = "0.1"
GLOBAL_SLOGANS = [
    "Now with letters!",
    "Free except electriciy bills",
    "Made in Russia",
    "Nya",
    "Please delete this",
    "Vanya, we need to implement connection"
]

print("===DISCARD===")
print("        ", GLOBAL_SLOGANS[ random.randint(0, len(GLOBAL_SLOGANS)-1 ) ] )
print("VER: ", GLOBAL_VER )

def cmd_help():
    print("help - show this text")
    print("connect - start connection")
    print("quit - stop discard'ing")
    print("host - start server")
    print("")
    print("")

def discard_tick():
    if GLOBAL_HOST:
        pass
    else:
        pass

cmd_help()
GLOBAL_NETWORK.createConnection( socket.gethostbyname(socket.gethostname()), random.randint(1000, 9999), "Nya" )
print("Socket created at ", GLOBAL_NETWORK.Address, ":", GLOBAL_NETWORK.Port)
while True:
    cmd = input("<Discard>: " )
    if cmd == "help":
        cmd_help()
    elif cmd == "quit":
        quit(0)
    elif cmd == "host":
        pass
