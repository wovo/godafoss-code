# ===========================================================================
#
# file     : gpio_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

# $$document( 0 )

# ===========================================================================

class gpio_oc( gf.pin_oc ):
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
        gf.pin_oc.__init__( self )

    # =======================================================================

    def read(
        self
    ) -> None:
        """
        """
        return self._pin.value()

    # =======================================================================

# ===========================================================================

