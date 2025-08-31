'''This module contains cli commands.'''

import random
import _thread
import socket
from typing import Callable
from dataclasses import dataclass
from . import globals
from . import network


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
    NET_INTERFACE = network.NetInter()
    NET_INTERFACE.hostMode = True
    NET_INTERFACE.updateGreetings()
    print("============================")
    print("Welcome to server setup wizard!")
    port = int(input("*Enter desired port: "))
    if globals.usingIpv6:
        adr = socket.getaddrinfo(socket.gethostname(),
                                 port, socket.AF_INET6)[0][4][0]
    else:
        adr = socket.gethostbyname(socket.gethostname())
    NET_INTERFACE.makeSocket(adr, port)
    NET_INTERFACE.choose_name()
    print("*Now hosting at "+NET_INTERFACE.address+":"+str(NET_INTERFACE.port))
    _thread.start_new_thread(NET_INTERFACE.serverTick, ())
    NET_INTERFACE.inputTick()


def enable_ipv6():
    '''Sets the `config.usingIpv6` to `True`.'''
    globals.usingIpv6 = True
    print("Now using IPv6!")


def disable_ipv6():
    '''Sets the `config.usingIpv6` to `False`.'''
    globals.usingIpv6 = False
    print("Now using IPv4!")


def connect():
    '''Runs the `NetInter` in the client mode.'''
    NET_INTERFACE = network.NetInter()
    print("============================")
    print("Welcome to server setup wizard!")
    if globals.usingIpv6:
        NET_INTERFACE.makeSocket(socket.getaddrinfo(socket.gethostname(
        ), 8080, socket.AF_INET6)[0][4][0], random.randint(1000, 9999))
    else:
        NET_INTERFACE.makeSocket(socket.gethostbyname(
            socket.gethostname()), random.randint(1000, 9999))
    NET_INTERFACE.choose_name()
    adr = input("*Enter desired address: ")
    if globals.usingIpv6:
        print(adr[0:(len(adr)-5)], adr[(len(adr)-4):len(adr)])
        NET_INTERFACE.connect(adr[0:(len(adr)-5)],
                              int(adr[(len(adr)-4):len(adr)]))
    else:
        NET_INTERFACE.connect(adr.split(":")[0], int(adr.split(":")[1]))
    _thread.start_new_thread(NET_INTERFACE.clientTick, ())
    NET_INTERFACE.inputTick()


commands = CommandList()

commands.add("help", Command(help, "explains what different commands do"))
commands.add("quit", Command(exit, "shuts down this application"))
commands.add("host", Command(host, "starts your very own server"))
commands.add("ipv6", Command(enable_ipv6, "sets IPv6 mode"))
commands.add("ipv4", Command(disable_ipv6, "sets IPv4 mode"))
commands.add("connect", Command(connect, "connects to the server"))
