# ===========================================================================
#
# file     : pin_out_from_two_pins.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_out_from_two_pins( gf.pin_out ):

    # =======================================================================

    def __init__( self, a, b ):
        gf.pin_out.__init__( self )
        self._a = a.as_pin_out()
        self._b = b.as_pin_out()

    # =======================================================================

    def write( self, value ):
        self._a.write( value )
        self._b.write( value )

    # =======================================================================

# ===========================================================================
