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
        if gf.running_micropython:    
            import machine
            self._pin = machine.Pin( pin_nr, machine.Pin.IN )
            gf.pin_in_out.__init__( self )
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode( GPIO.BCM )
            GPIO.setup( pin_nr, GPIO.IN )
            self._pin_nr = pin_nr                   

    # =======================================================================

    def direction_set_input( self ) -> None:
        if gf.running_micropython:      
            import machine
            self._pin.init( machine.Pin.IN )
        else:
            import RPi.GPIO as GPIO        
            GPIO.setup( self.pin_nr, GPIO.IN )        

    # =======================================================================

    def direction_set_output( self ) -> None:
        if gf.running_micropython:     
            import machine
            self._pin.init( machine.Pin.OUT )
        else:
            import RPi.GPIO as GPIO        
            GPIO.setup( self.pin_nr, GPIO.OUT )                  

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

