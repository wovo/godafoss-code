# ===========================================================================
#
# file     : _port_pins_write.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

def _port_pins_write( pins, value ):
    for pin in pins:
        pin.write( ( value & 0b1 ) == 0b1 )
        value = value >> 1

# ===========================================================================
