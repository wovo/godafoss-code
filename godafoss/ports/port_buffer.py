# ===========================================================================
#
# file     : port_buffer.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_buffer( gf.port_in_out ):
    """
    """

    def __init__(
        self,
        nr_of_pins: int
    ) -> None:
        self.values = 0
        self.directions = 0

        gf.port_in_out.__init__( self, nr_of_pins )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self.directions = directions

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self.values = values

    # =======================================================================

    def read( self ) -> int:
        return self.values

    # =======================================================================

# ===========================================================================

