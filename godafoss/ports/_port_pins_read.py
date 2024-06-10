# ===========================================================================
#
# file     : _port_pins_read.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

def _port_pins_read( pins ):

    result = 0
    for pin in pins[ :: -1 ]:
        result = result << 1
        if pin.read():
            result |= 0b1
    return result

# ===========================================================================
