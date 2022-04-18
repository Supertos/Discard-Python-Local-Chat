"""--------------------------------------------------
    network_base.py
    ---------------
    Provides base messaging functionality
    Year: 2022
    Author: Supertos
--------------------------------------------------"""

import socket
import random
import config
socket.setdefaulttimeout(0.1)

"""----------------------------------------------
    NetInter (Network Interface)
    Makes code less bloated
----------------------------------------------"""


class NetInter:
    def __init__(self):
        self.users = []
        self.greetings = []
        self.encoding = "utf-8"
        self.name = None
        self.message = None
        self.hostMode = False
        self.address = None
        self.port = None
        self.ipv6 = config.usingIpv6
        self.socket = None

    def choose_name(self):
        while True:
            name_temp = input("*Enter desired name: ")
            if len(name_temp) > config.NAME_SIZE_CHARS:
                print('name is too big')
            else:
                self.name = name_temp
                break

    def makeSocket(self, adr, port):
        self.address = adr
        self.port = port
        if self.ipv6:
            self.socket = socket.socket(socket.AF_INET6)
            self.socket.bind( (adr, port, 0, 0) )
        else:
            self.socket = socket.socket()
            self.socket.bind( (adr, port) )

    def broadcast(self, msg):
        for user in self.users:
            try:
                user[0].sendall( bytes( msg, self.encoding ))
            except ConnectionResetError:
                self.deleteUser(user[0], user[1])
                diconnectMsg = "*user " + user[3] + " disconnected"
                print(diconnectMsg)
                self.broadcast(self.encodeMsg(diconnectMsg))

    def deleteUser(self, host, port):
        for i in range(len(self.users)):
            if self.users[i][0] == host and self.users[i][1] == port:
                del self.users[i]
                break

    def updateGreetings(self):
        file = open("sv_greetings.txt")
        self.greetings = file.read().split("\n")
        file.close()

    def sendToServer(self, msg):
        try:
            self.socket.sendall( bytes( msg, self.encoding ))
        except ConnectionResetError:
            print("server ceased connection")
            pass  # TODO: disconnect from server and go back to main menu

    def connect(self, adr, port):
        try:
            if not self.ipv6:
                self.socket.connect( (adr, port) )
                self.sendToServer( self.encodeMsg("01", "") )
            else:
                self.socket.connect( (adr, port, 0, 0) )
                self.sendToServer( self.encodeMsg("01", "") )
        except (TimeoutError, socket.timeout):
            print("Unable to connect! Check if address and port are valid")
        except socket.error:
            print("Unknown error has occurred!")

    def encodeMsg(self, op, data):
        return op + self.name + " " * (config.NAME_SIZE_CHARS - len(self.name)) + data

    @staticmethod
    def decodeMsg(data):
        return [
            data[0: 2],
            data[2: config.NAME_SIZE_CHARS + 1].replace(" ", ""),
            data[config.NAME_SIZE_CHARS + 2: len(data)]
        ]

    def receiveMsgs(self):
        msgs = []
        for user in self.users:
            try:
                msg = self.decodeMsg( user[0].recv(8192).decode(self.encoding) )
                msg = [msg[0], msg[1], msg[2], user[2]]  # Save user ID to message for later usage
                msgs.append( msg )
            except (socket.error, TimeoutError, socket.timeout):
                pass
        return msgs

    def serverTick(self):
        while True:
            self.socket.listen(1)
            try:
                user = self.socket.accept()
                user = [user[0], user[1]]
                user.append(len( self.users ))  # Save its ID
                user.append( "" )  # Append username
                self.users.append( user )
            except (TimeoutError, socket.timeout):
                pass

            msgs = self.receiveMsgs()
            for msg in msgs:
                if msg[0] == "01":  # Greeting
                    self.users[ msg[3] ][3] = msg[1]
                    greet = self.greetings[random.randint(0, len(self.greetings)-1)].replace("{username}", msg[1])
                    print( "*"+greet )
                    self.broadcast( self.encodeMsg("02", "*"+greet) )
                elif msg[0] == "02":  # Server message
                    pass
                elif msg[0] == "03":  # User message
                    print( "<"+msg[1]+">: "+msg[2] )
                    self.broadcast( self.encodeMsg("02", "<"+msg[1]+">: "+msg[2]) )
                elif msg[0] == "04":  # Disconnect
                    pass  # TODO: There should be code to delete user

    def clientTick(self):
        while True:
            try:
                msg = self.decodeMsg( self.socket.recv( 8192 ).decode( self.encoding ) )
                if msg[0] == "01":  # Greeting
                    pass
                elif msg[0] == "02":  # Server message
                    print(msg[2])
                elif msg[0] == "03":  # User message
                    pass
                elif msg[0] == "04":  # Disconnect
                    pass
            except (TimeoutError, socket.timeout):
                pass

    def inputTick(self):
        while True:
            message = input()
            if message:
                if self.hostMode:
                    self.broadcast( self.encodeMsg("02", "<"+self.name+">: "+message ) )
                else:
                    self.sendToServer( self.encodeMsg("03", message) )