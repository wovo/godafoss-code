# ===========================================================================
#
# file     : port_oc__mirrored.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_oc__mirrored( gf.port_oc ):

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
