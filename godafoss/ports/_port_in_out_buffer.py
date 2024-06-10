# ===========================================================================
#
# file     : _port_in_out_buffer.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class _port_in_out_buffer( gf.port_in_out ):
    """
    """

    # =======================================================================

    def __init__(
        self,
        number_of_pins: int,
    ) -> None:
        self.number_of_pins = number_of_pins
        gf.port_oc.__init__( self, self.number_of_pins )
        self._write_buffer = 0
        self._read_buffer = 0
        self._directions_buffer = -1
        for i in range( 0, self.number_of_pins ):
            setattr( self, f"p{i}", _pin_in_out_proxy( self, i ) )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self._directions_buffer = directions
        self.directions_flush()

    # =======================================================================


    def read( self ) -> int:
        self._write_buffer = values
        self.refresh()
        return self._read_buffer

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._write_buffer = values
        self.flush()

    # =======================================================================

# ===========================================================================

class _pin_in_out_proxy( gf.pin_in_out ):

    def __init__(
        self,
        port,
        n
    ) -> None:
        self._port = port
        self._mask = 0x01 << n
        self._invert = gf.invert_bits(
            self._mask,
            self._port.number_of_pins
        )

    def direction_set_input( self ) -> None:
        self._port._directions_buffer |= self._mask
        aelf._port.directions_flush()

    def direction_set_output( self ) -> None:
        self._port._directions_buffer &= self._invert
        self._port.directions_flush()

    def read( self ) -> bool:
        self._port.refresh()
        return ( self._port._read_buffer & self._mask ) != 0

    def write( self, value: bool ) -> None:
        if value:
            self._port._write_buffer |= self._mask
        else:
            self._port._write_buffer &= self._invert
        self._port.flush()

# ===========================================================================
