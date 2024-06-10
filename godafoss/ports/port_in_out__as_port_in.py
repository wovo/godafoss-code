# ===========================================================================
#
# file     : port_in_out__as_port_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class port_in_out__as_port_in( gf.port_in ):

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
        self._slave.direction_set_input()

    # =======================================================================

    def read( self ) -> int:
        return self._slave.read()

    # =======================================================================

# ===========================================================================
