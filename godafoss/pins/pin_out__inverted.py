# ===========================================================================
#
# file     : pin_out__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_out__inverted( self ) -> "gf.pin_out":
    "inverse of the pin: writes the inverted level"

    # =======================================================================

    class _inverted( gf.pin_out ):

    # =======================================================================

        def __init__( self, pin ):
            gf.pin_out.__init__( self, self )
            self._pin = pin.as_pin_out()

        # ===================================================================

        def write( self, value ):
            self._pin.write( not value )

        # ===================================================================

    # =======================================================================

    return _inverted( self )

# ===========================================================================
