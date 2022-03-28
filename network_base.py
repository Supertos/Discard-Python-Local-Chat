"""--------------------------------------------------
    network_base.py
    ---------------
    Provides base messsaging functionality
    Year: 2022
    Author: Supertos
--------------------------------------------------"""

import socket
class network_interface:
    users = []
    def createConnection( self, adr, port, name ):
        self.socket     = socket.socket()
        self.Address    = adr
        self.Port       = port
        self.Name       = name
        self.socket.bind( (adr, port ) )
    """===Operation code: 1==="""
    def onUserConnection(self, msgdata):
        self.users[ msgdata[1]+":"+msgdata[2] ] = [ msgdata[3], msgdata[1], msgdata[2] ]
    def broadcast( self, data ):
        for user in self.users:
            self.socket.sendmsg(data, [(socket.SOL_SOCKET, socket.SCM_RIGHTS, user)])

    def connect( self, adr, port ):
        self.socket.connect( (adr, port ) )
        self.socket.sendmsg( GLOBAL_ENCODER.encode(1) )  #Just user data with opcode 1

"""------------------------------------------
    Encoded message structure
    -----------------------------------------
    Each symbol: 16 bytes
    Bits    | Symbols | Data
    0-255   | 0-15    | Address
    256-319 | 16-20   | Port
    320-575 | 20-35   | Username
    576-591 | 36      | Operation code
    591-... | 36-...  | Data
------------------------------------------"""

class msg_encoder:
    def bind_interface(self, interface):
        self.interface = interface
    def encode(self, opcode, data):
        Send = self.interface.Address + chr(0)*( 16-len(self.interface.Address))
        Send += str(self.interface.Port) + chr(0)*( 4-len(str(self.interface.Port)))
        Send += str(self.interface.Name) + chr(0)*( 16-len(str(self.interface.Name)))
        Send += str(opcode)
        Send += str(data)
        return Send
    def decode(self, msg ):
        Adr = msg[0:15].replace(chr(0), "")
        Port = msg[16:20].replace(chr(0), "")
        Name = msg[20:35].replace(chr(0), "")
        Code = msg[36].replace(chr(0), "")
        Data = msg[37:len(msg)].replace(chr(0), "")
        return [ Adr, Port, Name, Code, Data ]

