# ===========================================================================
#
# file     : gpio.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

# micropython
try:
    import machine
    from machine import Pin
except:
    pass   

# blinka
try:
 import board
 import digitalio
 import busio 
except:
    pass   

# raspberry pio RPi.GPIO    
try:
    import RPi.GPIO as GPIO    
except:
    pass   


# ===========================================================================

def _gpio_use(
    name: str
) -> None:

    """
    Use the classes _{name}_pin_* to create gpio pins.
    These classes must exist, and create an object 
    with the indicated attributes:
    
    _{name}_pin_in:
        pin: int | str
        read() -> int
        
    _{name}_pin_out:
        write( value: bool ) -> None
        
    _{name}_pin_in_out:
        pin: int | str
        read() -> int
        write( value: bool ) -> None
        _direction_set( direction: bool ) -> None
        
    _{name}_pin_oc:
        pin: int | str
        read() -> int
        write( value: bool ) -> None
        
    _{name}_pin_adc:
        pin: int | str
        read() -> fraction
    """
    
    print( f"gpio uses {name}" )
    for pin_type in ( "in", "out", "in_out", "oc", "adc" ):
        exec( 
            f"gpio_pin_{pin_type} = _{name}_pin_{pin_type}", 
            globals() 
        )


# ===========================================================================

def gpio_native() -> None:

    """
    use native gpio pins
    
    On MicroPython, use the chips GPIO pins.
    
    On a Raspberry Pi, use RPi.GPIO with BGM pin numbers 
    to access the GPIO pins.
    This requires root privilege.
    
    This is the default.
    """
    
    if gf.running_micropython:
        _gpio_use( "micropython" )
    else:
        try:
            GPIO.setwarnings( False )
            GPIO.setmode( GPIO.BCM )    
        except:
            pass        
        _gpio_use( "raspberry_pi" )

# ===========================================================================

def gpio_blinka() -> None:

    """
    use blinka to access gpio pins
    
    When a pin is created after calling this function, 
    it will use blinka to implement the pin operations.
    https://github.com/adafruit/blinka
    github.com/execuc/blinka
    https://pypi.org/project/pyu2f/
    """

    _gpio_use( "blinka" )


# ===========================================================================
#
# micropython native
#
# ===========================================================================

class _micropython_pin_in:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        _pin = machine.Pin(
            pin,
            machine.Pin.IN,
            machine.Pin.PULL_UP if pull_up else None
        )   
        self.read = _pin.value

    # =======================================================================
    

# ===========================================================================

class _micropython_pin_out:

    # =======================================================================

    def __init__(
        self,
        pin: int      
    ) -> None:
        self.pin = pin
        _pin = machine.Pin(
            pin,
            Pin.OUT
        )   
        self.write = _pin.value

    # =======================================================================
   

# ===========================================================================

class _micropython_pin_in_out:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        self.pull = machine.Pin.PULL_UP if pull_up else None
        self._pin = machine.Pin(
            pin,
            machine.Pin.IN,
            self.pull
        )   
        self.write = self.read = self._pin.value

    # =======================================================================
    
    def _direction_set( 
        self,
        direction: bool
    ) -> None:
        self._pin.init( 
            machine.Pin.IN if direction else machine.Pin.OUT,
            self.pull
        )

    # =======================================================================
    

# ===========================================================================

class _micropython_pin_oc:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        self._pin = machine.Pin(
            pin,
            machine.Pin.OPEN_DRAIN,
            machine.Pin.PULL_UP if pull_up else None
        )   
        self.write = self.read = self._pin.value

    # =======================================================================
    

# ===========================================================================

class _micropython_pin_adc:

    # =======================================================================

    def __init__(
        self,
        pin: "int | str"
    ):
        self.pin = pin
        self._adc = machine.ADC( machine.Pin( pin ) )

    # =======================================================================

    def read( 
        self 
    ) -> gf.fraction:
        return gf.fraction( self._adc.read_u16(), 65535 )

    # =======================================================================
    

# ===========================================================================
#
# blinka
#
# ===========================================================================

class _blinka_pin_in:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        _pin = digitalio.DigitalInOut(
            eval( f"board.D{pin}" ),
#            machine.Pin.IN,
#            machine.Pin.PULL_UP if pull_up else None
        )   
        _pin.direction = digitalio.Direction.OUTPUT
        self.read = _pin.value

    # =======================================================================  
    

# ===========================================================================

class _blinka_pin_out:

    # =======================================================================

    def __init__(
        self,
        pin: int      
    ) -> None:
        self.pin = pin
        _pin = digitalio.DigitalInOut(
            eval( f"board.D{pin}" ),
#            machine.Pin.IN,
        )   
        _pin.direction = digitalio.Direction.OUTPUT
        self.write = _pin.value

    # =======================================================================
   

# ===========================================================================

class _blinka_pin_in_out:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        print( "blinka" )
        self.pin = pin
#        self.pull = machine.Pin.PULL_UP if pull_up else None
        self._pin = digitalio.DigitalInOut(
            eval( f"board.D{pin}" ),
#            machine.Pin.IN,
#            self.pull
        )   
        self.write = self.read = self._pin.value

    # =======================================================================
    
    def _direction_set( 
        self,
        direction: bool
    ) -> None:
        self._pin.direction = (
            digitalio.Direction.INPUT 
            if direction 
            else digitalio.Direction.OUTPUT
        )

    # =======================================================================
    

# ===========================================================================

class _blinka_pin_oc:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        self._pin = machine.Pin(
            eval( f"blinka.GP{pin}" ),
            machine.Pin.OPEN_DRAIN,
            machine.Pin.PULL_UP if pull_up else None
        )   
        self.write = self.read = self._pin.value

    # =======================================================================
    

# ===========================================================================

class _blinka_pin_adc:

    # =======================================================================

    def __init__(
        self,
        pin: "int | str"
    ):
        self.pin = pin
        self._adc = machine.blinka.ADC( 
            eval( f"blinka.GP{pin}" )
        )

    # =======================================================================

    def read( 
        self 
    ) -> gf.fraction:
        return gf.fraction( self._adc.read_u16(), 65535 )

    # =======================================================================
    

# ===========================================================================
#
# Raspberry Pi GPIO
#
# ===========================================================================

class _raspberry_pi_pin_in:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin   
        GPIO.setup( 
            pin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP if pull_up else GPIO.PUD_OFF 
        )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return RPi.GPIO.input( self.pin ) == RPi.GPIO.LOW

    # =======================================================================
    
    
# ===========================================================================

class _raspberry_pi_pin_out:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin   
        GPIO.setup( pin, GPIO.OUT )

    # =======================================================================

    def write(
        self,
        value: "bool | int"
    ) -> None:
        GPIO.output( 
           self.pin, 
           GPIO.HIGH if value else GPIO.LOW 
        )    

    # =======================================================================
    
    
# ===========================================================================

class _raspberry_pi_pin_in_out:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        self.pull = GPIO.PUD_UP if pull_up else GPIO.PUD_OFF
        GPIO.setup( 
            pin, 
            GPIO.IN, 
            pull_up_down = self.pull 
        )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return RPi.GPIO.input( self.pin ) == RPi.GPIO.LOW    

    # =======================================================================

    def write(
        self,
        value: "bool | int"
    ) -> None:
        GPIO.output( 
           self.pin, 
           GPIO.HIGH if value else GPIO.LOW 
        )    

    # =======================================================================
    
    def _direction_set( 
        self,
        direction: "bool | int"
    ) -> None:
        GPIO.setup(
            self.pin, 
            GPIO.IN if direction else GPIO.OUT,
            pull_up_down = self.pull
        )

    # =======================================================================
    
    
# ===========================================================================

class _raspberry_pi_pin_oc:

    # =======================================================================

    def __init__(
        self,
        pin: int,
        pull_up: bool = False        
    ) -> None:
        self.pin = pin
        self.pull = GPIO.PUD_UP if pull_up else GPIO.PUD_OFF 
        GPIO.setup( 
            pin, 
            GPIO.IN, 
            self.pull
        )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return RPi.GPIO.input( self.pin ) == RPi.GPIO.LOW        

    # =======================================================================

    def write(
        self,
        value: "bool | int"
    ) -> None:
        if value:
            GPIO.setup( 
                self.pin, 
                GPIO.IN, 
                pull_up_down = self.pull
            )        
        else:  
            GPIO.setup( 
                self.pin, 
                GPIO.OUT
            ) 
            GPIO.output( 
               self.pin, 
               GPIO.LOW 
            )    

    # =======================================================================
    
    
# ===========================================================================

class _raspberry_pi_pin_adc: 

    def __init__( 
        self, 
        *args, 
        **kwargs 
    ) -> None:   
        raise Exception( "No ADC pin aviable on a Raspberry Pi" )

    
# ===========================================================================

# set the default    
gpio_native()  
#gpio_blinka()


# ===========================================================================
