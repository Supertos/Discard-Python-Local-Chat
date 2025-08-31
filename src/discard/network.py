"""--------------------------------------------------
    network_base.py
    ---------------
    Provides base messaging functionality
    Year: 2022
    Author: Supertos
--------------------------------------------------"""

import socket
socket.setdefaulttimeout(0.1)

NAME_SIZE_CHARS = 24


class NetInter:
    '''
    This is a kitchen sink class for the application.

    It implements both the server's host and the server's client.
    '''

    def __init__(self, name: str, socket: socket.socket, is_host: bool):
        self.name = name
        self.socket = socket
        self.is_host = is_host
        self.users = []
        self.encoding = "utf-8"

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
                self.delete_user(user[0], user[1])
                diconnectMsg = "*user " + user[3] + " disconnected"
                print(diconnectMsg)
                self.broadcast(encode_msg(diconnectMsg, self.name))

    def delete_user(self, host, port):
        '''
        In host mode this function will remove the specified 
        user from the list of tracked users.

        This function is not used in client mode.
        '''
        for i in range(len(self.users)):
            if self.users[i][0] == host and self.users[i][1] == port:
                del self.users[i]
                break

    def send_to_server(self, msg):
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
            self.socket.connect((adr, port))
            self.send_to_server(encode_msg("01", "", self.name))
        except (TimeoutError, socket.timeout):
            print("Unable to connect! Check if address and port are valid")
        except socket.error:
            print("Unknown error has occurred!")

    def receive_msgs(self):
        '''
        In host mode this function will check for new messages from 
        all of the connected clients and return the list of decoded
        messages with some additional information.

        This function is not used in client mode.
        '''
        msgs = []
        for user in self.users:
            try:
                msg = decode_msg(user[0].recv(8192).decode(self.encoding))
                # Save user ID to message for later usage
                msg = [msg[0], msg[1], msg[2], user[2]]
                msgs.append(msg)
            except (socket.error, TimeoutError, socket.timeout):
                pass
        return msgs

    def server_loop(self):
        '''
        Host execution loop. This should run on a separate thread.
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

            msgs = self.receive_msgs()
            for msg in msgs:
                # See `NetInter.encodeMsg` for opcode specification.
                if msg[0] == "01":
                    self.users[msg[3]][3] = msg[1]
                    greet = random_greeting(msg[1])
                    print("*"+greet)
                    self.broadcast(encode_msg("02", "*"+greet, self.name))
                elif msg[0] == "02":
                    pass
                elif msg[0] == "03":
                    print("<"+msg[1]+">: "+msg[2])
                    self.broadcast(encode_msg(
                        "02", "<"+msg[1]+">: "+msg[2], self.name))
                elif msg[0] == "04":
                    raise NotImplementedError(
                        "Opcode `04` is not supported yet.")

    def client_loop(self):
        '''
        Client execution loop. This should run on a separate thread.
        '''
        while True:
            try:
                msg = decode_msg(self.socket.recv(
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

    def input_loop(self):
        '''
        Keeps prompting the user to enter a message and 
        keeps sending it to all other users on the server.
        '''
        while True:
            message = input()
            if message:
                if self.is_host:
                    self.broadcast(encode_msg(
                        "02", "<"+self.name+">: "+message, self.name))
                else:
                    self.send_to_server(encode_msg("03", message, self.name))


def random_greeting(username: str) -> str:
    '''Generates a random greeting with the specified username.'''
    from random import choice
    greetings = [
        "{username} has joined the party!",
        "Say hi to {username}!",
        "Howdy {username} how it's going?",
        "{username} is now server's member!",
    ]
    return choice(greetings).replace('{username}', username)


def encode_msg(op, data, name):
    '''
    Encodes the message before sending it.

    Encoding consists of the the opcode, the name and
    the data parts. Opcode part specifies the kind of 
    message to be sent and should be exactly two 
    characters long. Name part specifes the user's 
    preferred name and shold not exceed 
    `NAME_SIZE_CHARS` characters in length. 
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
    return op + name + " " * (NAME_SIZE_CHARS - len(name)) + data


def decode_msg(data):
    '''Decodes the message after receiving it.'''
    return [
        data[0: 2],
        data[2: NAME_SIZE_CHARS + 1].replace(" ", ""),
        data[NAME_SIZE_CHARS + 2: len(data)]
    ]
