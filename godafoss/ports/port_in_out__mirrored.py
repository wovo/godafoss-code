# ===========================================================================
#
# file     : port_in_out__mirrored.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class port_in_out__mirrored( gf.port_in_out ):

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
        self._slave.directions_set(
            gf.mirror_bits(
                directions,
                self.number_of_pins
            )
        )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write(
            gf.mirror_bits(
                values,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read( self ) -> int:
        return gf.mirror_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================

# ===========================================================================
