# ===========================================================================
#
# file     : pins.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (godafoss.license)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================
#
# pin superclasses (used in type hints)
#
# ===========================================================================

class can_pin_in:

    """
    :class:`~godafoss.pin_in` compatible

    An object of this class has an as_pin_in() member function
    that returns a :class:`~godafoss.pin_in` version of the object.
    """

    pass


# ===========================================================================

class can_pin_out:

    """
    :class:`~godafoss.pin_out` compatible

    An object of this class has an as_pin_out() member function
    that returns a :class:`~godafoss.pin_out` version of the object.
    """

    pass


# ===========================================================================

class can_pin_in_out:

    """
    :class:`~godafoss.pin_in_out` compatible

    An object of this class has an as_pin_out() member function
    that returns a :class:`~godafoss.pin_in_out` version of the object.

    """

    pass


# ===========================================================================

class can_pin_oc:

    """
    :class:`~godafoss.pin_oc` compatible

    An object of this class has an as_pin_out() member function
    that returns a :class:`~godafoss.pin_oc` version of the object.
    """

    pass


# ===========================================================================
#
# pin_in
#
# ===========================================================================

class pin_in(
    can_pin_in
):

    """
    digital input pin

    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_in" )

    This is digital input pin: an object from which you can
    read() a bool value.

    :param pin: (int | str | :class:`~can_pin_in` | None )
        Either a gpio pin identification (int or str),
        a :class:`~can_pin_in` object
        (from which a pin_in is creatred using its as_pin_in method()),
        or None (which causes a dummy pin to be created).
    """

    # =======================================================================

    def __init__(
        self,
        pin: gf.Union[ int, str, None, can_pin_in ]
    ):

        if pin is not None:

            try:
                self.worker = pin.as_pin_in()

            except:
                self.pin_nr = pin
                self.worker = _gpio_in( self.pin_nr )

            # to speed things up: use the workers method directly
            self.read = self.worker.read

    # =======================================================================

    def read(
        self
    ) -> bool:

        """
        the level on the pin

        :result: (bool)
            the level read from the pin
        """

        return self.value

    # =======================================================================

    def as_pin_in(
        self
    ) -> "pin_in":

        """
        the pin itself
        """

        return self

    # =======================================================================

    def inverted(
        self
    ) -> "pin_in":


        """
        inverted version of the pin: reads the inverted value
        """

        return _pin_in_inverted( self )

    # =======================================================================

    def demo(
        self,
        period: int = 500_000,
        iterations = None
    ) -> None:

        """
        print the pin level
        """

        pin = self.as_pin_in()

        for _ in gf.repeater( iterations ):
            print( pin.read() )
            gf.sleep_us( period )

    # =======================================================================


# ===========================================================================
#
# pin_out
#
# ===========================================================================

class pin_out(
    can_pin_out
):

    """
    digital input out

    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_out" )

    This is digital output pin: an object from which you can
    can write() a digital level.

    :param pin: (int | str | gf.can_pin_out | None )
        Either a (int or str) gpio pin identification,
        or a pin that has an as_pin_in_out method(),
        or None (return a dummy pin).

    Two pins that each have an as_pin_out() method can be added
    (+ operator) to yield a
    $$ref( "pin_in_out" )
    that writes to both pins.
    """

    # =======================================================================

    def __init__(
        self,
        pin: gf.Union[ None, int, str, can_pin_out ]
    ):

        if pin is not None:

            try:
                self.worker = pin.as_pin_out()

            except:
                self.pin_nr = pin
                self.worker = _gpio_out( self.pin_nr )

            # to speed things up: use the workers method directly
            self.write = self.worker.write

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:

        """
        set the pin output level

        :param value: (bool)
            the level to output to the pin
        """

        self.value = bool( value )

    # =======================================================================

    def as_pin_out( self ) -> "pin_out":

        """
        the pin itself
        """

        return self

    # =======================================================================

    def __add__(
        self,
        other: can_pin_out
    ) -> "pin_out":

         return _write_to_both( self, other )

    # =======================================================================

    def inverted(
        self
    ) -> "pin_out":

        """
        inverse of the pin: writes the inverted level
        """

        return _pin_out_inverted( self )

    # =======================================================================

    def demo(
        self,
        *args,
        **kwargs
    ):

        """
        blink the pin, see $$ref( "blink" )
        """

        blink( self, *args, **kwargs )

    # =======================================================================

    def pulse(
        self,
        *args,
        **kwargs
    ) -> None:
        """
        issue a (high) on the pin, see $$ref( "pulse" )
        """

        pulse( self, *args, **kwargs )


# ===========================================================================
#
# pin_in_out
#
# ===========================================================================

class pin_in_out(
    can_pin_in,
    can_pin_out,
    can_pin_in_out,
    can_pin_oc
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_in_out" )

    digital input output pin

    :param pin: (int | str | gf.can_pin_in_out | None )
        Either a (int or str) gpio pin identification,
        or a pin that has an as_pin_in_out method()
        (
        $$ref( "pin_in_out" )
        or
        $$ref( "pin_oc" )
        ),
        or None (return a dummy pin).

    When the direction has been set to output,
    a write() determines the pin level.
    When the direction has been set to input,
    a read() returns the pin level.

    Two pins that each have an as_pin_out() method can be added
    (+ operator) to yield a
    $$ref( "port_in_out" )
    that writes to both pins.
    """

    # =======================================================================

    def __init__(
        self,
        pin: "int | str | None | can_pin_in_out"
    ):
        print( "343", pin )
        if pin is not None:

            try:
                self.worker = pin.as_pin_in_out()

            except:
                self.pin_nr = pin
                self.worker = _gpio_in_out( self.pin_nr )

            # to speed things up: use the workers methods directly
            self._direction_set = self.worker._direction_set
            self.write = self.worker.write
            self.read = self.worker.read
            self.direction_set_input()

    # =======================================================================

    def _direction_set(
        self,
        value: bool
    ) -> None:
        pass

    # =======================================================================

    def direction_set_output(
        self
    ) -> None:

        """
        set the pin direction to output
        """

        self._input = False
        self._direction_set( False )

    # =======================================================================

    def direction_set_input(
        self
    ) -> None:

        """
        set the pin direction to input
        """

        self._input = True
        self._direction_set( True )

    # =======================================================================

    def direction_set(
        self,
        direction: gf.Union[ bool, int ]
    ) -> None:

        """
        set the pin direction, 1 = input, 0 = output
        """
        
        self._input = direction
        self._direction_set( direction )

    # =======================================================================

    def direction_is_input(
        self
    ) -> bool:

        """
        return whether the current pin direction is input
        """

        return self._input

    # =======================================================================

    def direction_is_output(
        self
    ) -> bool:

        """
        return whether the current pin direction is output
        """

        return not self._input

    # =======================================================================

    def read(
        self
    ) -> bool:

        """
        when the pin direction has been set to input:
        return the level on the pin

        :result: (bool)
            the level read from the pin
        """

        return self.value

    # =======================================================================

    def write(
        self,
        value: gf.Union[ bool, int ]
    ) -> None:

        """
        when the pin direction has been set to output:
        set the pin output level

        :param value: (bool)
            the level to output to the pin
        """

        self.value = bool( value )

    # =======================================================================

    def as_pin_in(
        self
    ) -> "gf.pin_in":

        """
        the input-only version of the pin
        """

        return _pin_in_out_as_pin_in( self )

    # =======================================================================

    def as_pin_out(
        self
    ) -> "gf.pin_out":

        """
        the output-only version of the pin
        """

        return _pin_in_out_as_pin_out( self )

    # =======================================================================

    def as_pin_in_out(
        self
    ) -> "pin_in_out":

        """
        the pin itself
        """

        return self

    # =======================================================================

    def as_pin_oc( self ) -> "gf.pin_oc":
        "the open-collector version of the pin"

        return _pin_in_out_as_pin_oc( self )

    # =======================================================================

    def inverted(
        self
    ) -> "gf.pin_in_out":

        """
        a pin that will read and write the inverted level
        """

        return _pin_in_out_inverted( self )

    # =======================================================================

    def demo(
        self,
        *args,
        **kwargs
    ):

        """
        blink the pin, see $$ref( "blink" )
        """

        blink( self, *args, **kwargs )

    # =======================================================================

    def pulse(
        self,
        *args,
        **kwargs
    ) -> None:
        """
        issue a (high)
        $$ref( "pulse" )
        on the pin
        """

        self.as_pin_out().pulse( *args, **kwargs )

    # =======================================================================

    def __add__(
        self,
        other: can_pin_out
    ) -> "pin_out":

        return _write_to_both( self, other )

    # =======================================================================


# ===========================================================================
#
# pin_oc
#
# ===========================================================================

class pin_oc(
    can_pin_oc,
    can_pin_in,
    can_pin_out,
    can_pin_in_out,
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_oc" )

    open-collector (or more likely, open-drain) input output pin

    :param pin: (int | str | gf.can_pin_oc | None )
        Either a (int or str) gpio pin identification,
        or a pin that has an as_pin_oc method()
        (
        $$ref( "pin_in_out" )
        or
        $$ref( "pin_oc" )
        ),
        or None (return a dummy pin).

    Two pins that each have an as_pin_out() method can be added
    (+ operator) to yield a
    $$ref( "port_in_out" )
    that writes to both pins.
    """

    # =======================================================================

    def __init__(
        self,
        pin: "int | str | None | gf.can_pin_oc"
    ):

        if pin is not None:

            try:
                self.worker = pin.as_pin_oc()

            except:
                self.pin_nr = pin
                self.worker = gf.gpio_oc( self.pin_nr )

            # to speed things up: use the workers methods directly
            self.write = self.worker.write
            self.read = self.worker.read

    # =======================================================================

    def read(
       self
    ) -> bool:

        """
        return the level on the pin

        :result: (bool)
            the level read from the pin

        When a 0 has been written to the pin, a 0 will be read unless
        there is some serious hardware trouble.
        When a 1 has been written, the level on the pin will be read.
        """

        return self.value

    # =======================================================================

    def write(
        self,
        value: gf.Union[ bool, int ]
    ) -> None:

        """
        set the pin output level

        :param value: (bool)
            the level to output to the pin

        When False is written,
        the pin hardware will pull the output level low.
        When True is written,
        the pin hardware will let the pin level float.
        """

        self.value = bool( value )

    # =======================================================================

    def __add__(
        self,
        other: can_pin_out
    ) -> "pin_out":

        return _write_to_both( self, other )

    # =======================================================================

    def as_pin_oc(
        self
    ) -> "pin_oc":

        return self

    # =======================================================================

    def as_pin_in( self ):

        """input version of the pin"""

        return _pin_oc_as_pin_in( self )

    # =======================================================================

    def as_pin_in_out( self ):

        """
        the input-output version of the pin

        Note that is a pseudo (input-) output: writing a zero to
        it will pull the output low, but writing a one to it will float
        the output (not pull it high, as a read input-output pin would).
        """

        return _pin_oc_as_pin_in_out( self )

    # =======================================================================

    def as_pin_out(
        self
    ) -> "pin_out":

        """
        the pin as output-only pin
        """

        return _pin_oc_as_pin_out( self )

    # =======================================================================

    def inverted( self ) -> "gf.pin_oc":

        """
        inverse of the pin: reads and writes the inverted level
        """

        return _pin_oc_inverted( self )

    # =======================================================================

    def demo(
        self,
        *args,
        **kwargs
    ):

        """
        blink the pin, see $$ref( "blink" )
        """

        blink( self, *args, **kwargs )

    # =======================================================================

    def pulse(
        self,
        *args,
        **kwargs
    ) -> None:
        """
        issue a (high)
        $$ref( "pulse" )
        on the pin
        """

        pulse( self, *args, **kwargs )

    # =======================================================================

    def __add__(
        self,
        other
    ) -> "pin_out":

        return _add( self, other )

    # =======================================================================


# ===========================================================================
#
# write to two pins
#
# ===========================================================================

class _write_to_both( pin_out ):

    # =======================================================================

    def __init__( self, a, b ):
        pin_out.__init__( self, self )
        self._a = a.as_pin_out()
        self._b = b.as_pin_out()

    # =======================================================================

    def write( self, value ):
        self._a.write( value )
        self._b.write( value )

    # =======================================================================


# ===========================================================================
#
# inversion decorators
#
# ===========================================================================

class _pin_in_inverted( pin_in ):

    # =======================================================================

    def __init__( self, pin ) -> None:
        pin_in.__init__( self, self )
        self._pin = pin

    # =======================================================================

    def read( self ) -> bool:
        return not self._pin.read()

    # =======================================================================


# ===========================================================================

class _pin_out_inverted( pin_out ):

    # =======================================================================

    def __init__( self, pin ):
        pin_out.__init__( self, self )
        self._pin = pin.as_pin_out()

    # =======================================================================

    def write( self, value ):
        self._pin.write( not value )

    # =======================================================================


# ===========================================================================

class _pin_in_out_inverted( pin_in_out ):

    # =======================================================================

    def __init__(
        self,
        pin
    ):
        self._pin = pin
        pin_in_out.__init__( self, self )
        # can steal!

    # =======================================================================

    def _direction_set(
        self,
        direction: bool
    ) -> None:
        self._pin._direction_set( direction )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return not self._pin.read()

    # =======================================================================

    def write(
        self,
        value: bool
    ) ->  None:
        self._pin.write( not value )

    # =======================================================================


# ===========================================================================

class _pin_oc_inverted( pin_oc ):

    # =======================================================================

    def __init__( self, pin ):
        self._pin = pin
        pin_oc.__init__( self, self )
        # can steal!

    # =======================================================================

    def read( self ) -> bool:
        return not self._pin.read()

    # =======================================================================

    def write(
        self,
        value: bool
    ):
        self._pin.write( not value )

    # =======================================================================


# ===========================================================================
#
# pin type conversion decorators
#
# ===========================================================================

class _pin_in_out_as_pin_in( pin_in ):

    # =======================================================================

    def __init__(
        self,
        pin: "gf.pin_in_out"
    ) -> None:
        gf.pin_in.__init__( self, self )
        self._pin = pin
        self._pin.direction_set_input()

    # =======================================================================

    def read( self ) -> bool:
        return self._pin.read()

    # =======================================================================


# ===========================================================================

class _pin_in_out_as_pin_out( pin_out ):

    # =======================================================================

    def __init__(
        self,
        pin: pin_in_out
    ) -> None:
        print( f"create pin_out {self} from {pin}" )
        #breakpoint()
        self._pin = pin
        self._pin.direction_set_output()
        gf.pin_out.__init__( self, self )
        print( "done" )

        # speed things up
        self.write = self._pin.write

    # =======================================================================


# ===========================================================================

class _pin_in_out_as_pin_oc( pin_oc ):

    # =======================================================================

    def __init__(
        self,
         pin
    ) -> None:
        gf.pin_oc.__init__( self, self )
        self._pin = pin

    # =======================================================================

    def read(
        self
    ) -> bool:
        return self._pin.read()

    # =======================================================================

    def write(
        self,
        value
    ) -> None:
        if value:
            self._pin.direction_set_input()
        else:
            self._pin.direction_set_output()
            self._pin.write( False )

    # =======================================================================


# ===========================================================================

class _pin_oc_as_pin_in( pin_in ):

    def __init__(
        self,
        pin
    ):
        pin_in.__init__( self, self )
        self._pin = pin
        self._pin.write( 1 )

    # =======================================================================

    def read(
        self
    ):
        return self._pin.read()

    # =======================================================================


# ===========================================================================

class _pin_oc_as_pin_in_out( pin_in_out ):

    # =======================================================================

    def __init__(
        self,
        pin
    ) -> None:
        self._pin = pin
        pin_in_out.__init__( self, self )

    # =======================================================================

    def _direction_set(
        self,
        value: bool = True
    ) -> None:

        if value:
            self._pin.write( 1 )

        else:
            # It is debatable whether this is needed, but
            # it makes testing more regular.
            self._pin.write( 0 )

    # =======================================================================

    def write(
        self,
        value
    ) -> None:
        self._pin.write( value )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return self._pin.read()

    # =======================================================================


# ===========================================================================

class _pin_oc_as_pin_out( pin_out ):

    # =======================================================================

    def __init__(
        self,
        pin
    ) -> None:
        gf.pin_out.__init__( self, self )
        self._pin = pin

    # =======================================================================

    def write(
        self,
        value
    ) -> None:
        self._pin.write( value )

    # =======================================================================


# ===========================================================================
#
# gpio
#
# ===========================================================================

class _gpio_in( pin_in ):
    """
    chip GPIO pin used as input

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int,
        pull_up: bool = False
    ) -> None:
        if gf.running_micropython:
            import machine
            self._pin = machine.Pin(
                pin_nr,
                machine.Pin.IN,
                machine.Pin.PULL_UP if pull_up else None
            )
            pin_in.__init__( self, self )
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

class _gpio_out( pin_out ):
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

        pin_out.__init__( self, self )

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

    def gpio_out_hosted(
    self: pin_out
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

        pin_out.__init( self )
        return


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

class _gpio_in_out( pin_in_out ):
    """
    chip GPIO pin used as input

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int,
        pull_up: bool = False
    ) -> None:
        self.pull_up = pull_up
        if gf.running_micropython:
            import machine
            self._pin = machine.Pin(
                pin_nr,
                machine.Pin.IN,
                machine.Pin.PULL_UP if self.pull_up else None
            )
            pin_in_out.__init__( self, None )
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode( GPIO.BCM )
            GPIO.setup( pin_nr, GPIO.IN )
            self._pin_nr = pin_nr

    # =======================================================================

    def _direction_set( 
        self,
        direction: bool
    ) -> None:
        if gf.running_micropython:
            import machine
            
            if direction:
                self._pin.init( 
                    machine.Pin.IN,
                    machine.Pin.PULL_UP if self.pull_up else None
                )
            else:    
                self._pin.init( 
                    machine.Pin.OUT 
                )      
            
        else:
            import RPi.GPIO as GPIO
            
            if direction:
                # pull-up?
                GPIO.setup( self.pin_nr, GPIO.IN )
            else:    
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

class _gpio_oc( pin_oc ):
    """
    chip GPIO pin used as input

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int,
        pull_up: bool = False
    ) -> None:
        import machine
        print( pin_nr )
        self._pin = machine.Pin(
            pin_nr,
            machine.Pin.IN,
            machine.Pin.PULL_UP if pull_up else None
        )
        pin_oc.__init__( self )

    # =======================================================================

    def read(
        self
    ) -> None:
        """
        """
        return self._pin.value()

    # =======================================================================


# ===========================================================================
#
# common pin functions
#
# ===========================================================================

def blink(
    pin: gf.Union[ int, str, None, can_pin_out ],
    period: int = 500_000,
    high_time = None,
    low_time = None,
    iterations = None
) -> None:

    """
    blink on the pin

    Blink on the pin,
    with {high_time} high level and {low_time}
    (defaults to high_time) low level,
    for the specified number of {iterations}
    (defaults to infinite).

    Times are in us (microseconds).
    """

    high_time = high_time or period // 2
    low_time = low_time or high_time

    p = gf.pin_out( pin )
    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            p.pulse( 0, 0 )
            gf.report_memory_and_time()

        p.pulse( high_time, low_time )


# ===========================================================================

def pulse(
    pin: gf.Union[ int, str, None, can_pin_out ],
    high_time: int,
    low_time: int = 0
) -> None:

    """
    output a (positive) pulse on the pin

    $$see_also( "pin_out","pin_in_out", "pin_oc" )

    make the pin high, wait for high_time,
    make the pin low, and wait for low_time

    $$insert_image( "pulse", 300 )

    :param high_time: (int)
        duration of the high part of the pulse

    :param low_time: (int)
        duration of the low part of the pulse (defaults to 0)

    The times are in us (microseconds).
    """

    p = pin_out( pin )

    p.write( True )
    if high_time != 0:
        gf.sleep_us( high_time )

    p.write( False )
    if low_time != 0:
        gf.sleep_us( low_time )

# ===========================================================================

