# ===========================================================================
#
# file     : pin_oc__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_oc__inverted( self ) -> "gf.pin_oc":
    "inverse of the pin: reads and writes the inveted level"

    # =======================================================================

    class _inverted( gf.pin_oc ):

        # ===================================================================

        def __init__( self, pin ):
            self._pin = pin
            gf.pin_oc.__init__( self, self )
            # can steal!

        # ===================================================================

        def read( self ) -> bool:
            return not self._pin.read()

        # ===================================================================

        def write(
            self,
            value: bool
        ):
            self._pin.write( not value )

        # ===================================================================

    # =======================================================================

    return _inverted( self )

# ===========================================================================
