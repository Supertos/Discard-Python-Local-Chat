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
    '''
    This is a kitchen sink class for the application.

    It implements both the server's host and the server's client.
    '''

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
        '''Runs the prompt loop to let user choose their username.'''
        while True:
            name_temp = input("*Enter desired name: ")
            if len(name_temp) > config.NAME_SIZE_CHARS:
                print('name is too big')
            else:
                self.name = name_temp
                break

    def makeSocket(self, adr, port):
        '''
        Initializes a socket.

        - If `NetInter` is a host than this socket will be used 
        to communicate with the clients.
        - If `NetInter` is a client than this socket will be
        used to communicate with the host.
        '''
        self.address = adr
        self.port = port
        if self.ipv6:
            self.socket = socket.socket(socket.AF_INET6)
            self.socket.bind((adr, port, 0, 0))
        else:
            self.socket = socket.socket()
            self.socket.bind((adr, port))

    def broadcast(self, msg):
        '''
        In host mode this function will send the specified
        message to all of the currently available clients.

        This function is not used in client mode.
        '''
        for user in self.users:
            try:
                user[0].sendall(bytes(msg, self.encoding))
            except ConnectionResetError:
                self.deleteUser(user[0], user[1])
                diconnectMsg = "*user " + user[3] + " disconnected"
                print(diconnectMsg)
                self.broadcast(self.encodeMsg(diconnectMsg))

    def deleteUser(self, host, port):
        '''
        In host mode this function will remove the specified 
        user from the list of tracked users.

        This function is not used in client mode.
        '''
        for i in range(len(self.users)):
            if self.users[i][0] == host and self.users[i][1] == port:
                del self.users[i]
                break

    def updateGreetings(self):
        '''
        Parses and splits `sv_greetings.txt` on newlines, writes the 
        resulting values to `self.greetings`.
        '''
        file = open("sv_greetings.txt")
        self.greetings = file.read().split("\n")
        file.close()

    def sendToServer(self, msg):
        '''
        In client mode this function will send the message
        to the server. Message should be properly encoded
        with `self.encodeMsg`.

        This function is not used in host mode.
        '''
        try:
            self.socket.sendall(bytes(msg, self.encoding))
        except ConnectionResetError:
            print("server ceased connection")
            raise NotImplementedError(
                "Disconnecting from the server is not yet implemented")

    def connect(self, adr, port):
        '''
        In client mode this function will try to 
        connect the client to the host.

        This function is not used in host mode.
        '''
        try:
            if not self.ipv6:
                self.socket.connect((adr, port))
                self.sendToServer(self.encodeMsg("01", ""))
            else:
                self.socket.connect((adr, port, 0, 0))
                self.sendToServer(self.encodeMsg("01", ""))
        except (TimeoutError, socket.timeout):
            print("Unable to connect! Check if address and port are valid")
        except socket.error:
            print("Unknown error has occurred!")

    def encodeMsg(self, op, data):
        '''
        Encodes the message before sending it.

        Encoding consists of the the opcode, the name and
        the data parts. Opcode part specifies the kind of 
        message to be sent and should be exactly two 
        characters long. Name part specifes the user's 
        preferred name and shold not exceed 
        `config.NAME_SIZE_CHARS` characters in length. 
        Data part contains the message's text.

        Opcodes:

        `01` - client sends this to the host after connecting to it.
        The host should respond by broadcasting a greeting for this
        client.
        `02` - host sends this to the clients after recieving a 
        message with `03` opcode from one of the clients. Host 
        should ignore the messages with this opcode.
        `03` - client sends this to the host whenever they want to 
        send a message to everyone in the server. Host should respond
        to this message by broadcasting same message with an `02`
        opcode. Clients should ignore the messages with this opcode.
        `04` - Not yet implemented. Client sends this message to the
        host befor disconnecting from it. Clients should ignore the
        messages with this opcode.
        '''
        return op + self.name + " " * (config.NAME_SIZE_CHARS - len(self.name)) + data

    @staticmethod
    def decodeMsg(data):
        '''Decodes the message after receiving it.'''
        return [
            data[0: 2],
            data[2: config.NAME_SIZE_CHARS + 1].replace(" ", ""),
            data[config.NAME_SIZE_CHARS + 2: len(data)]
        ]

    def receiveMsgs(self):
        '''
        In host mode this function will check for new messages from 
        all of the connected clients and return the list of decoded
        messages with some additional information.

        This function is not used in client mode.
        '''
        msgs = []
        for user in self.users:
            try:
                msg = self.decodeMsg(user[0].recv(8192).decode(self.encoding))
                # Save user ID to message for later usage
                msg = [msg[0], msg[1], msg[2], user[2]]
                msgs.append(msg)
            except (socket.error, TimeoutError, socket.timeout):
                pass
        return msgs

    def serverTick(self):
        '''
        Host execution loop. This should run on a separate thread.

        Despite the naming this funcion never returns.
        '''
        while True:
            self.socket.listen(1)
            try:
                user = self.socket.accept()
                user = [user[0], user[1]]
                user.append(len(self.users))  # Save its ID
                user.append("")  # TODO: Append username?
                self.users.append(user)
            except (TimeoutError, socket.timeout):
                pass

            msgs = self.receiveMsgs()
            for msg in msgs:
                # See `NetInter.encodeMsg` for opcode specification.
                if msg[0] == "01":
                    self.users[msg[3]][3] = msg[1]
                    greet = self.greetings[random.randint(
                        0, len(self.greetings)-1)].replace("{username}", msg[1])
                    print("*"+greet)
                    self.broadcast(self.encodeMsg("02", "*"+greet))
                elif msg[0] == "02":
                    pass
                elif msg[0] == "03":
                    print("<"+msg[1]+">: "+msg[2])
                    self.broadcast(self.encodeMsg(
                        "02", "<"+msg[1]+">: "+msg[2]))
                elif msg[0] == "04":
                    raise NotImplementedError(
                        "Opcode `04` is not supported yet.")

    def clientTick(self):
        '''
        Client execution loop. This should run on a separate thread.

        Despite the naming this funcion never returns.
        '''
        while True:
            try:
                msg = self.decodeMsg(self.socket.recv(
                    8192).decode(self.encoding))
                # See `NetInter.encodeMsg` for opcode specification.
                if msg[0] == "01":
                    pass
                elif msg[0] == "02":
                    print(msg[2])
                elif msg[0] == "03":
                    pass
                elif msg[0] == "04":
                    pass
            except (TimeoutError, socket.timeout):
                pass

    def inputTick(self):
        '''
        Prompts the user to enter a message and 
        sends it to all other users on the server.
        '''
        while True:
            message = input()
            if message:
                if self.hostMode:
                    self.broadcast(self.encodeMsg(
                        "02", "<"+self.name+">: "+message))
                else:
                    self.sendToServer(self.encodeMsg("03", message))
