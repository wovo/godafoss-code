# ===========================================================================
#
# file     : port_oc__as_pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class port_oc__as_pin_out( gf.pin_out ):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.pin_out.__init__( self )

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        self._slave.write( -1 if value else 0 )

    # =======================================================================


# ===========================================================================
