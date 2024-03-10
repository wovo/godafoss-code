# ===========================================================================
#
# file     : port_in_out__as_port_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_in_out__as_port_oc( gf.port_oc ):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.port_oc.__init__(
            self,
            self._slave.number_of_pins
        )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write( values )
        self._slave.directions_set( values )

    # =======================================================================

    def read( self ) -> int:
        return self._slave.read()

    # =======================================================================

# ===========================================================================
