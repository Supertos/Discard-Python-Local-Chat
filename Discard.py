"""-------------------------------------------------
    Discard
    --------------------
    Year: 2022
    Author: Supertos
    Notes:
        Send messages like a boss
-------------------------------------------------"""

import network_base
import random

GLOBAL_ENCODER = network_base.msg_encoder()
GLOBAL_NETWORK = network_base.network_interface()

GLOBAL_ENCODER.bind_interface( GLOBAL_NETWORK )

GLOBAL_VER = "0.1"
GLOBAL_SLOGANS = [
    "Now with letters!",
    "Free except electriciy bills",
    "Made in Russia",
    "Nya",
    "Please delete this",
    "Vanya, we need to implement connection stuff"
]

print("===DISCARD===")
print("        ", GLOBAL_SLOGANS[ random.randint(0, len(GLOBAL_SLOGANS)-1 ) ] )
print("VER: ", GLOBAL_VER )
