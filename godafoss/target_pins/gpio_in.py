# ===========================================================================
#
# file     : gpio_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class gpio_in( gf.pin_in ):
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
        if gf.running_micropython:    
            import machine
            self._pin = machine.Pin( pin_nr, machine.Pin.IN )
            gf.pin_in.__init__( self )
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode( GPIO.BCM )
            GPIO.setup( pin_nr, GPIO.IN )
            self._pin_nr = pin_nr               

    # =======================================================================

    def read(
        self
    ) -> None:
        """
        """
        if gf.running_micropython:        
            return self._pin.value()
        else:
            return GPIO.input( self._pin_nr )

    # =======================================================================

# ===========================================================================

