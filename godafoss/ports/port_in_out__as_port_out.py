# ===========================================================================
#
# file     : port_in_out__as_port_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class port_in_out__as_port_out( gf.port_out ):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.port_out.__init__(
            self,
            self._slave.number_of_pins
        )
        self._slave.direction_set_output()

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write( value )

    # =======================================================================

# ===========================================================================
