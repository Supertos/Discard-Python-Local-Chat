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
global GLOBAL_ENCODER
global GLOBAL_NETWORK
GLOBAL_ENCODER = network_base.msg_encoder()

GLOBAL_NETWORK = network_base.network_interface()

GLOBAL_ENCODER.bind_interface( GLOBAL_NETWORK )

global GLOBAL_HOST
global GLOBAL_CHAT
global GLOBAL_VER
GLOBAL_VER = "0.2"
GLOBAL_CHAT = False
GLOBAL_HOST = False

GLOBAL_MSG = ""

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
    print("connect - connect to server")
    print("")

def input_tick():
    global GLOBAL_MSG
    while True:
        GLOBAL_MSG = input("< "+GLOBAL_NETWORK.Name+" >:")

def discard_tick():
    global GLOBAL_MSG
    while True:
        if not GLOBAL_CHAT: return

        if GLOBAL_MSG != "":
            print("<", GLOBAL_NETWORK.Name, ">:", GLOBAL_MSG)
            if GLOBAL_HOST:
                print("<", GLOBAL_NETWORK.Name ,">:", GLOBAL_MSG)
                GLOBAL_NETWORK.broadcast( GLOBAL_ENCODER.encode(0, "< "+GLOBAL_NETWORK.Name+" >: "+GLOBAL_MSG) )
            else:
                GLOBAL_NETWORK.sendToServer( GLOBAL_ENCODER.encode(0, "< "+GLOBAL_NETWORK.Name+" >: "+GLOBAL_MSG) )
            GLOBAL_MSG = ""
        if GLOBAL_HOST:
            GLOBAL_NETWORK.socket.listen(1)
            New_User = GLOBAL_NETWORK.socket.accept()
            if New_User:
                print(New_User[1], "connected to server!")
        for user in GLOBAL_NETWORK.users:
            data = user.recvmsg(2048)
            if data[3] == 1:
                GLOBAL_NETWORK.onUserDesignation( data )
            elif data[3] == 0:
                GLOBAL_NETWORK.onMessage( data )
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
        GLOBAL_CHAT = True
        GLOBAL_HOST = True
        _thread.start_new_thread( discard_tick, () )
        _thread.start_new_thread( input_tick, () )
        break
    elif cmd == "connect":
        print("===Welcome to connection establish wizard!===")
        GLOBAL_NETWORK.Name = input("Enter your name:")
        adr = input("Enter desired address:")
        port = input("Enter desired port:")
        GLOBAL_NETWORK.connect(adr, port)
        GLOBAL_CHAT = True
while True:
    pass
