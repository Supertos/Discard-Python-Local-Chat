'''This module contains cli commands.'''

import random
import _thread
import socket
from typing import Callable
from dataclasses import dataclass
from . import network


def choose_name() -> str:
    '''Runs the prompt loop to let user choose their username.'''
    while True:
        name = input("*Enter desired name: ")
        if len(name) > network.NAME_SIZE_CHARS:
            print('name is too big')
        else:
            return name


def make_socket(adr: str, port: int) -> socket.socket:
    '''Constructs and initializes a new socket.'''
    soc = socket.socket()
    soc.bind((adr, port))
    return soc


def help():
    '''Prints help for the user.'''
    print("============================")
    commands.list_commands()
    print("============================")


def exit():
    '''Shuts down the application.'''
    quit(0)


def host():
    '''Runs the `NetInter` in host mode.'''
    print("============================")
    print("Welcome to server setup wizard!")
    adr = socket.gethostbyname(socket.gethostname())
    port = int(input("*Enter desired port: "))
    soc = make_socket(adr, port)
    name = choose_name()
    net = network.NetInter(name, soc, True)
    print(f'*Now hosting at {adr} : {port}')
    _thread.start_new_thread(net.server_loop, ())
    net.input_loop()


def connect():
    '''Runs the `NetInter` in the client mode.'''
    print("============================")
    print("Welcome to server setup wizard!")
    adr = socket.gethostbyname(socket.gethostname())
    port = random.randint(1000, 9999)
    soc = make_socket(adr, port)
    name = choose_name()
    net = network.NetInter(name, soc, False)
    full_adr = input("*Enter desired address: ").split(":")
    net.connect(full_adr[0], int(full_adr[1]))

    _thread.start_new_thread(net.client_loop, ())
    net.input_loop()


@dataclass
class Command:
    '''
    Wrapper for cli commands.

    - `self.function` - an associated function for the command.
    - `self.description` - explanation of what the command does.
    '''

    function: Callable[[], None]
    description: str


class CommandList:
    '''Helper class to manage cli commands.'''

    def __init__(self):
        self.commands: dict[str, Command] = dict()

    def add(self, name: str, command: Command):
        '''Adds a command to the list.'''
        self.commands[name] = command

    def try_execute(self, name: str) -> bool:
        '''
        Executes the command with the specified name if 
        it was added to the list. 

        Returns `True` or `False` based on if the command 
        with the specified name was found or not.
        '''
        if name not in self.commands:
            return False

        self.commands[name].function()
        return True

    def list_commands(self):
        '''Prints the added commands.'''
        for (name, command) in self.commands.items():
            print(f'{name} - {command.description}.')


commands = CommandList()

commands.add("help", Command(help, "explains what different commands do"))
commands.add("quit", Command(exit, "shuts down this application"))
commands.add("host", Command(host, "starts your very own server"))
commands.add("connect", Command(connect, "connects to the server"))
