# ===========================================================================
#
# file     : make_port_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class make_port_in_out( gf.port_in_out ):
    """
    digital output port from pins

    A port_out is constructed from a number of pins that are outputs
    or can function as outputs.
    """

    def __init__(
        self,
        *args
    ) -> None:
        # create the list of the pins
        try:
            self._pins = [
                gf.make_pin_in_out( pin )
                    for pin in gf.make_tuple( *args )
            ]
        except AttributeError:
            raise AttributeError from None

        gf.port_in_out.__init__( self, len( self._pins  ) )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        gf._port_pins_directions( self._pins, directions )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        gf._port_pins_write( self._pins, values )

    # =======================================================================

    def read( self ) -> int:
        return gf._port_pins_read( self._pins )

    # =======================================================================

# ===========================================================================

