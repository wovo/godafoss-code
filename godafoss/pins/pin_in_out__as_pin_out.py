# ===========================================================================
#
# file     : pin_in_out__as_pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out__as_pin_out( gf.pin_out ):

    # =======================================================================

    def __init__(
        self,
        pin: "gf.pin_in_out"
    ) -> None:
        gf.pin_out.__init__( self )
        self._pin = pin
        self._pin.direction_set_output()

    # =======================================================================

    def write( self, value ) -> None:
        self._pin.write( value )

    # =======================================================================

# ===========================================================================
