# ===========================================================================
#
# file     : pin_oc__as_pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_oc__as_pin_out( self ) -> "pin_out":
    "the pin as output-only pin"

    class _as_pin_out( gf.pin_out ):

        # ===================================================================

        def __init__( self, pin ) -> None:
            gf.pin_out.__init__( self, self )
            self._pin = pin

        # ===================================================================

        def write( self, value ) -> None:
            self._pin.write( value )

        # ===================================================================

    return _as_pin_out( self )

# ===========================================================================

