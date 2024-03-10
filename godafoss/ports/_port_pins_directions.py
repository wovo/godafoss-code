# ===========================================================================
#
# file     : _port_pins_directions.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

def _port_pins_directions( pins, directions ):
    for pin in pins:
        if ( ( directions & 0b1 ) == 0b1 ):
            pin.direction_set_input()
        else:
            pin.direction_set_output()
        directions = directions >> 1

# ===========================================================================
