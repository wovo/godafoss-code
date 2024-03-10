# ===========================================================================
#
# file     : port_out__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_out__inverted( gf.port_out ):

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

# ===========================================================================
