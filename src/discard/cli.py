'''This module contains the entry point for the application.'''

import argparse
import random
import _thread
import socket
from . import network
from . import __version__


def make_socket(adr: str, port: int) -> socket.socket:
    '''Constructs and initializes a new socket.'''
    soc = socket.socket()
    soc.bind((adr, port))
    return soc


def version_command():
    '''`version` command.'''
    print(f'Discard version {__version__}')


def host_command(name: str, port: int):
    '''`host` command.'''
    addr = socket.gethostbyname(socket.gethostname())
    soc = make_socket(addr, port)
    net = network.NetInter(name, soc, True)
    _thread.start_new_thread(net.server_loop, ())
    print(f'*Now hosting at {addr}:{port}')
    net.input_loop()


def connect_command(name: str, addr: str, port: int):
    '''`connect` command.'''
    own_adr = socket.gethostbyname(socket.gethostname())
    own_port = random.randint(1000, 9999)
    soc = make_socket(own_adr, own_port)
    net = network.NetInter(name, soc, False)
    net.connect(addr, port)
    _thread.start_new_thread(net.client_loop, ())
    print(f'*Now connected to {addr}:{port}')
    net.input_loop()


def main():
    '''Entry point for the application.'''
    parser = argparse.ArgumentParser(description=f'Discard')
    subparser = parser.add_subparsers(
        dest='command',
        help='Available Commands')

    subparser.add_parser('version', help='Print version information')

    host_parser = subparser.add_parser('host', help='Host a server')
    host_parser.add_argument('name', help='The username to use')
    host_parser.add_argument('port', type=int, help='Desired port to host on')

    connect_parser = subparser.add_parser(
        'connect',
        help='Connect to a server')
    connect_parser.add_argument('name', help='The username to use')
    connect_parser.add_argument(
        'addr',
        help='IPv4 address of the host written as X.X.X.X')
    connect_parser.add_argument('port', type=int, help='Port to connect to.')

    args = parser.parse_args()

    if args.command == 'version':
        version_command()
    elif args.command == 'host':
        host_command(args.name, args.port)
    elif args.command == 'connect':
        connect_command(args.name, args.addr, args.port)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
