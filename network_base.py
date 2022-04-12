"""--------------------------------------------------
    network_base.py
    ---------------
    Provides base messaging functionality
    Year: 2022
    Author: Supertos
--------------------------------------------------"""

import socket
socket.setdefaulttimeout(0.1)

"""----------------------------------------------
    NetInter (Network Interface)
    Makes code less bloated
----------------------------------------------"""
class NetInter:
    users = []
    coding = "utf-8"
    name = "Katya"
    def makeSocket(self, adr, port):
        self.socket = socket.socket()
        self.address = adr
        self.port = port

        self.socket.bind( (adr, port) )

    def broadcast(self, msg):
        for user in self.users:
            user.sendall( bytes( msg, self.coding ))

    def sendToServer(self, msg):
        self.socket.sendall( bytes( msg, self.coding ))

    def connect(self, adr, port):
        try:
            self.socket.connect( (adr, port))
        except TimeoutError:
            print("Unable to connect! Check if address and port are valid")
        except socket.error:
            print("Unknown error has occurred!")

    def encodeMsg(self, op, data):
        return op+self.name+" "*(24-len(self.name))+data

    def decodeMsg(self, data):
        return {data[0], data[1:24].replace(" ", ""), data[1:len(data)]}

    def receiveMsgs(self):
        msgs = []
        for user in self.users:
            try:
                msg = self.decodeMsg( user.recv(8192).decode(self.coding) )
                msgs.append( msg )
            except (socket.error, TimeoutError):
                pass
        return msgs
