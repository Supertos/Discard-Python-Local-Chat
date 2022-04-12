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
import socket
import _thread

GLOBAL_ENCODER = network_base.msg_encoder()
GLOBAL_NETWORK = network_base.network_interface()
GLOBAL_ENCODER.bind_interface( GLOBAL_NETWORK )
GLOBAL_NETWORK.linkEncoder( GLOBAL_ENCODER )

GLOBAL_VER = "0.2"
GLOBAL_CHAT = False
GLOBAL_HOST = False

GLOBAL_MSG = ""

GLOBAL_SLOGANS = [
    "Now with letters!",
    "Free except electricity bills",
    "Made in Russia",
    "Nya",
    "Please delete this",
    "Vanya, we need to implement connection",
    "Vanya, you're fired!"
]

print("===DISCARD===")
print("        ", GLOBAL_SLOGANS[ random.randint(0, len(GLOBAL_SLOGANS)-1 ) ] )
print("VER: ", GLOBAL_VER )

def cmd_help():
    print("============================")
    print("help - show this text")
    print("connect - start connection")
    print("quit - stop discard'ing")
    print("host - start server")
    print("connect - connect to server")
    print("============================")

def input_tick():
    global GLOBAL_MSG
    while True:
        GLOBAL_MSG = input("< "+GLOBAL_NETWORK.Name+" >:")

def discard_tick():
    global GLOBAL_MSG
    global GLOBAL_CHAT
    global GLOBAL_NETWORK
    global GLOBAL_ENCODER

    while True:
        if not GLOBAL_CHAT: return #Stop this thread when we finish chatting
        
        """===Messaging==="""
        if GLOBAL_MSG: #We have a message we want to send
            print("<", GLOBAL_NETWORK.Name, ">:", GLOBAL_MSG)
            if GLOBAL_HOST:
                GLOBAL_NETWORK.broadcast( GLOBAL_ENCODER.encode(0, "< "+GLOBAL_NETWORK.Name+" >: "+GLOBAL_MSG) )
            else:
                GLOBAL_NETWORK.sendToServer( GLOBAL_ENCODER.encode(0, "< "+GLOBAL_NETWORK.Name+" >: "+GLOBAL_MSG) )
            GLOBAL_MSG = ""
        """===Listening==="""
        if GLOBAL_HOST: #We're host
            GLOBAL_NETWORK.socket.listen(1)
            try:
                New_User = GLOBAL_NETWORK.socket.accept()
                GLOBAL_NETWORK.users.append(New_User[0])
                print(New_User[1], "connected to server!")
            except socket.error:
                pass
            except ( socket.error, TimeoutError):
                pass

            for user in GLOBAL_NETWORK.users:   #Receive messages
                try:
                    ld = user.recv(8192).decode("utf-8")    #We're getting bytes so we need to decode 'em into string
                    data = GLOBAL_ENCODER.decode( ld )  #Then parse into array
                    if data[3] == 1:    #Opcodes
                        GLOBAL_NETWORK.onUserDesignation( data )
                    elif data[3] == 0:
                        GLOBAL_NETWORK.onMessage( data )
                except ( socket.error, TimeoutError):
                    pass
        else:   #We're client
            try:
                ld = GLOBAL_NETWORK.socket.recv(8192).decode("utf-8")   #Receive data from server only
                data = GLOBAL_ENCODER.decode(ld)
                if data[3] == 1:
                    GLOBAL_NETWORK.onUserDesignation(data)
                elif data[3] == 0:
                    GLOBAL_NETWORK.onMessage(data)
            except (socket.error, TimeoutError):
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
        if not GLOBAL_NETWORK.connect(adr, int(port)):
            print("Connected!")
            GLOBAL_CHAT = True
            _thread.start_new_thread(discard_tick, ())
            _thread.start_new_thread(input_tick, ())
while True:
    pass
