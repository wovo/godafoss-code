# ===========================================================================
#
# file     : _port_oc_buffer.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class _port_oc_buffer( gf.port_oc ):
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
        for i in range( 0, self.number_of_pins ):
            setattr( self, f"p{i}", _pin_oc_proxy( self, i ) )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._write_buffer = values
        self.flush()

    # =======================================================================

# ===========================================================================

class _pin_oc_proxy( gf.pin_oc ):

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

    def write( self, value ) -> None:
        if value:
            self._port._write_buffer |= self._mask
        else:
            self._port._write_buffer &= self._invert
        self._port.flush()

