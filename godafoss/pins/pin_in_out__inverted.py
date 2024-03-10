# ===========================================================================
#
# file     : pin_in_out__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out__inverted( gf.pin_in_out ):
    """proxy that inverses a pin_in_out"""

    # =======================================================================

    def __init__( self, pin ):
        gf.pin_in_out.__init__( self )
        self._pin = pin

    # =======================================================================

    def direction_set_input( self ) -> None:
        self._pin.direction_set_input()

    # =======================================================================

    def direction_set_output( self ) -> None:
        self._pin.direction_set_output()

    # =======================================================================

    def read( self ) -> bool:
        return not self._pin.read()

    # =======================================================================

    def write( self, value ):
        self._pin.write( not value )

    # =======================================================================

# ===========================================================================
