# ===========================================================================
#
# file     : port_oc__as_port_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_oc__as_port_in( gf.port_in ):

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
        return self._slave.read()

    # =======================================================================

# ===========================================================================
