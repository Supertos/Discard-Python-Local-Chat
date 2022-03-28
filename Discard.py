"""-------------------------------------------------
    Discard
    --------------------
    Year: 2022
    Author: Supertos
    Notes:
        Send messages like a boss
-------------------------------------------------"""

import network_base

GLOBAL_ENCODER = network_base.msg_encoder()
GLOBAL_NETWORK = network_base.network_interface()

GLOBAL_ENCODER.bind_interface( GLOBAL_NETWORK )