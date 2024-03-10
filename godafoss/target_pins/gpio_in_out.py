# ===========================================================================
#
# file     : gpio_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class gpio_in_out( gf.pin_in_out ):
    """
    chip GPIO pin used as input

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int
    ) -> None:
        import machine
        self._pin = machine.Pin( pin_nr, machine.Pin.IN )
        gf.pin_in_out.__init__( self )

    # =======================================================================

    def direction_set_input( self ) -> None:
        import machine
        self._pin.init( machine.Pin.IN )

    # =======================================================================

    def direction_set_output( self ) -> None:
        import machine
        self._pin.init( machine.Pin.OUT )

    # =======================================================================

    def read(
        self
    ) -> None:
        """
        """
        return self._pin.value()

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin value

        :param value: (bool)
            the new pin value (level)
        """
        self._pin.value( value )

    # =======================================================================

# ===========================================================================

