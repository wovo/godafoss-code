# ===========================================================================
#
# file     : gpio_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class gpio_out( gf.pin_out ):
    """
    chip GPIO pin used as output

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int
    ) -> None:
        import machine
        self._pin = machine.Pin( pin_nr, machine.Pin.OUT )
        gf.pin_out.__init__( self )

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

