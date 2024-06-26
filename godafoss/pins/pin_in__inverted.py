# ===========================================================================
#
# file     : pin_in__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_in__inverted( self ):
    "inverted version of the pin: reads the inverted value"

    # =======================================================================

    class _inverted( gf.pin_in ):

        # ===================================================================

        def __init__( self, pin ) -> None:
            gf.pin_in.__init__( self, self )
            self._pin = pin

        # ===================================================================

        def read( self ) -> bool:
            return not self._pin.read()

        # ===================================================================

    # =======================================================================

    return _inverted( self )

# ===========================================================================
