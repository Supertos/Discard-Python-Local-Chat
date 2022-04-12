"""--------------------------------------------------
    network_base.py
    ---------------
    Provides base messsaging functionality
    Year: 2022
    Author: Supertos
--------------------------------------------------"""

import socket

class net_inter:
    users = []
    coding = "utf-8"
    def makeSocket(self, adr, port):
        self.socket = socket.socket()
        self.adress = adr
        self.port = port

        self.socket.settimeout(0.1)
        self.socket.bind( (adr, port) )

    def broadcast(self, msg):
        for user in self.users:
            user.sendall( bytes( msg, coding ))

    def sendToServer(self, msg):
        self.socket.sendall( bytes( msg, coding ))

    def connect(self, adr, port):
        try:
            self.socket.connect( (adr, port))
        except TimeoutError:
            print("Unable to connect! Check if adress and port are valid")
        except (socket.error):
            print("Unknown error has occured!")