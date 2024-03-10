# ===========================================================================
#
# file     : pin_in__demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_in__demo(
    pin, # : "gf.pin_in" | "gf.pin_in_out" | "gf.pin_oc",
    period: int = 500_000,
    iterations = None
) -> None:

    pin = pin.as_pin_in()

    for _ in gf.repeater( iterations ):
        print( pin.read() )
        gf.sleep_us( period )

# ===========================================================================
