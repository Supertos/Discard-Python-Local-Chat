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

"""------------------------------------------
    Encoded message structure
    -----------------------------------------
    Each symbol: 16 bytes
    Bits    | Data
    0-255   | Address
    256-319 | Port
    320-575 | Username
    576-591 | Operation code
    591-... | Data
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

enc = msg_encoder()
network = network_interface()

network.createConnection( socket.gethostbyname(socket.gethostname()), 9090, "Nya" )
