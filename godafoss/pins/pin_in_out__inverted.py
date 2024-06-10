# ===========================================================================
#
# file     : pin_in_out__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_in_out__inverted( self ) -> "gf.pin_in_out":
    """a pin that will read and write the inverted level"""

    # =======================================================================

    class _inverted( gf.pin_in_out ):

    # =======================================================================

     def __init__( self, pin ):
        self._pin = pin
        gf.pin_in_out.__init__( self, self )
        # can steal!

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

     def write(
        self,
        value: bool
     ):
        self._pin.write( not value )

    # =======================================================================

    return _inverted( self )

# ===========================================================================
