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
        if gf.running_micropython:
            import machine
            self._pin = machine.Pin( pin_nr, machine.Pin.OUT )
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode( GPIO.BCM )
            GPIO.setup( pin_nr, GPIO.OUT )
            self._pin_nr = pin_nr   
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
        if gf.running_micropython:
            self._pin.value( value )
        else:   
            import RPi.GPIO as GPIO
            GPIO.output( self._pin_nr, GPIO.HIGH if value else GPIO.LOW ) 

    # =======================================================================

# ===========================================================================

