# ===========================================================================
#
# file     : pin_oc__as_pin_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_oc__as_pin_in( gf.pin_in ):

    # =======================================================================

    def __init__( self, pin ):
        gf.pin_in.__init__( self )
        self._pin = pin
        self._pin.write( 1 )

    # =======================================================================

    def read( self ):
        return self._pin.read()

    # =======================================================================

# ===========================================================================

