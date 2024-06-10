# ===========================================================================
#
# file     : gpio_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

# $$document( 0 )

# ===========================================================================

class gpio_out:
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
        self._pin_nr = pin_nr

        if gf.running_micropython:
            import machine
            self._pin = machine.Pin( self._pin_nr, machine.Pin.OUT )

        else:
            gf.gpio_out_hosted( self )

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

