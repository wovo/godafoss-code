# ===========================================================================
#
# file     : port_oc__as_port_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_oc__as_port_in_out( gf.port_in_out ):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.port_in_out.__init__(
            self,
            self._slave.number_of_pins
        )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self.write( directions )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write( values )
        self._slave.write( values )

    # =======================================================================

    def read( self ) -> int:
        return self._slave.read()

    # =======================================================================

# ===========================================================================
