# ===========================================================================
#
# file     : port_in__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_in__inverted( gf.port_in ):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.port_in.__init__(
            self,
            self._slave.number_of_pins
        )

    # =======================================================================

    def read( self ) -> int:
        return gf.invert_bits( self._slave.read(), self.number_of_pins )

    # =======================================================================

# ===========================================================================
