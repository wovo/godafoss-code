# ===========================================================================
#
# file     : pin_oc__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_oc__inverted( gf.pin_oc ):

    # =======================================================================

    def __init__( self, pin ):
        gf.pin_oc.__init__( self )
        self._pin = pin.as_pin_oc()

    # =======================================================================

    def read( self ) -> bool:
        return not self._pin.read()

    # =======================================================================

    def write( self, value ):
        self._pin.write( not value )

    # =======================================================================

# ===========================================================================
