# ===========================================================================
#
# file     : pin_in__demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_in__demo(
    self,
    period: int = 500_000,
    iterations = None
) -> None:
    "logs the pin level"

    pin = self.as_pin_in()

    for _ in gf.repeater( iterations ):
        print( pin.read() )
        gf.sleep_us( period )

# ===========================================================================
