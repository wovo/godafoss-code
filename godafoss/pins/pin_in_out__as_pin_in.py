# ===========================================================================
#
# file     : pin_in_out__as_pin_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out__as_pin_in( gf.pin_in ):

    # =======================================================================

    def __init__(
        self,
        pin: "gf.pin_in_out"
    ) -> None:
        gf.pin_in.__init__( self )
        self._pin = pin
        self._pin.direction_set_input()

    # =======================================================================

    def read( self ) -> bool:
        return self._pin.read()

    # =======================================================================

# ===========================================================================
