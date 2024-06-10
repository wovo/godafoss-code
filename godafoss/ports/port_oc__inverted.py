# ===========================================================================
#
# file     : port_oc__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class port_oc__inverted( gf.port_oc ):

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

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write(
            gf.invert_bits(
                value,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read( self ) -> int:
        return gf.invert_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================

# ===========================================================================
