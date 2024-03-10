# ===========================================================================
#
# file     : pin_in_out__as_pin_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out__as_pin_oc( gf.pin_oc ):

    # =======================================================================

    def __init__( self, pin ) -> None:
        gf.pin_oc.__init__( self )
        self._pin = pin

    # =======================================================================

    def read( self ) -> bool:
        return self._pin.read()

    # =======================================================================

    def write( self, value ) -> None:
        if value:
            self._pin.direction_set_input()
        else:
            self._pin.direction_set_output()
            self._pin.write( False )

    # =======================================================================

# ===========================================================================
