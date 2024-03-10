# ===========================================================================
#
# file     : make_pin_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

def make_pin_in(
    pin
) -> "gf.pin_out":
    """

    """

    if pin is None:
        pin = gf.pin_dummy()

    elif isinstance( pin, int ):
        if pin < 0:
            pin = gf.pin_dummy()
        else:
            pin = gf.gpio_in( pin )

    return pin.as_pin_in()

