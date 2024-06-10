# ===========================================================================
#
# file     : gpio_out_hosted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def gpio_out_hosted(
    self: gf.pin_out
):

    # =======================================================================
    #
    # u2if
    #
    # =======================================================================

    try:

        from machine import u2if, Pin

        self._pin = Pin( u2if.GP3, Pin.OUT )

        self.write = lambda self, value: \
            self._pin.value( Pin.HIGH if value else Pin.LOW )

    except ModuleNotFoundError:
        pass

    # =======================================================================
    #
    # RPi.GPIO
    #
    # =======================================================================

    try:
        import RPi.GPIO as GPIO
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self._pin_nr, GPIO.OUT )

        self.write = lambda self, value: \
            GPIO.output( self._pin_nr, GPIO.HIGH if value else GPIO.LOW )

        return

    except ModuleNotFoundError:
        pass

    # =======================================================================
    #
    # blinka using adafruit u2if clone
    #
    # =======================================================================


    try:
        import digitalio
        import board

        p = eval( f"board.GP{self._pin_nr}" )

        self._pin = digitalio.DigitalInOut( p )
        self._pin.direction = digitalio.Direction.OUTPUT

        setattr(
            self,
            "write",
            lambda value: setattr( self._pin, "value", value )
        )

        return

    except ModuleNotFoundError:
        pass

    raise Exception( "no GPIO support available" )




# ===========================================================================

