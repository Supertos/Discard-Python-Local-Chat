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
    users   = []
    greetings = []
    coding  = "utf-8"
    name    = "Katya"
    message = ""
    def makeSocket(self, adr, port):
        self.socket     = socket.socket()
        self.address    = adr
        self.port       = port

        self.socket.bind( (adr, port) )

    def broadcast(self, msg):
        for user in self.users:
            user.sendall( bytes( msg, self.coding ))

    def updateGreetings(self):
        with open("sv_greetings.txt") as file:
            self.greetings = file.read().split("\n")
            file.close()


    def sendToServer(self, msg):
        self.socket.sendall( bytes( msg, self.coding ))

    def connect(self, adr, port):
        try:
            self.socket.connect( (adr, port) )
            self.sendToServer( self.encodeMsg("01", "") )
        except TimeoutError:
            print("Unable to connect! Check if address and port are valid")
        except socket.error:
            print("Unknown error has occurred!")

    def encodeMsg(self, op, data):
        return op+self.name+" "*(24-len(self.name))+data

    def decodeMsg(self, data):
        return {data[0:2], data[2:25].replace(" ", ""), data[26:len(data)]}

    def receiveMsgs(self):
        msgs = []
        for user in self.users:
            try:
                msg = self.decodeMsg( user.recv(8192).decode(self.coding) )
                msg[3] = user[2]    #Save user ID to message for later usage
                msgs.append( msg )
            except (socket.error, TimeoutError):
                pass
        return msgs

    def serverTick(self):
        while True:
            self.socket.listen(1)
            try:
                user = self.socket.accept()
                user.append(len( self.users ) + 1)  #Save it's ID
                user.append( "" )   #Append username
                self.users.append( user )
            except TimeoutError:
                pass

            msgs = self.receiveMsgs()
            for msg in msgs:
                if msg[0] == "01": #Greeting
                    self.users[ msg[3] ] = msg[1]
                    greet = self.greetings[random.randint(0, len(self.greetings))].replace("{username}", msg[1])
                    print( "*"+greet )
                    self.broadcast( self.encodeMsg("02", "*"+greet) )
                elif msg[0] == "02": #Server message
                    pass
                elif msg[0] == "03": #User message
                    print( "<"+msg[1]+">: "+msg[2] )
                    self.broadcast( self.encodeMsg("02", "<"+msg[1]+">: "+msg[2]) )
                elif msg[0] == "04": #Disconnect
                    pass #There should be code to delete user

    def clientTick(self):
        while True:
            msgs = self.socket.recv( 8192 )
            for msg in msgs:
                if msg[0] == "01":  # Greeting
                    pass
                elif msg[0] == "02":  # Server message
                    print(msg[2])
                elif msg[0] == "03":  # User message
                    pass
                elif msg[0] == "04":  # Disconnect
                    pass

    def inputTick(self):
        while True:
            message = input("<"+self.name+">")
            if message:
                if hostMode:
                    self.broadcast( self.encode("02", "<"+self.name+">: "+message ) )
                else:
                    self.broadcast( self.encode("03", message) )
