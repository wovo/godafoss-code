# ===========================================================================
#
# file     : interfaces.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class adc:
    """
    abstract analog input

    An adc reads a voltage level and returns it
    as a fraction of the full scale.

    examplesx::
    x$insert_example( "test_adc.py", "adc examples", 1 )

    """

    def adc__read( self ) -> "gf.fraction":
       """
       Read and return the adc value as a fraction of its full scale.
       """

       raise NotImplementedError

# ===========================================================================

def adcx__inverted( self ) -> "gf.adc":

    # =======================================================================

    def __init__(
        self,
        pin: gf.adc
    ):
        self._pin = pin
        gf.adc.__init__( self )

    # =======================================================================

    def read( self ) -> "gf.fraction":
        return - self._pin.read()

    # =======================================================================

    def inverted( self ) -> "gf.adc":
        return self._pin

    # =======================================================================

# ===========================================================================


# ===========================================================================


# ===========================================================================

# ===========================================================================

class dac:
    """
    an analog output pin

    A write causes a dac to output the specified voltage.
    The value written is a fraction of the full scale output.

    $macro_insert invertible

    examples
    $insert_example( "test_dac.py", "dac examples", 1 )
    """

    # =======================================================================

    def __init__( self ) -> None:
        invertible.__init__( self )

    # =======================================================================

    def write(
        self,
        value: gf.fraction
    ) -> None:
        """
        write the adc value as a fraction

        :param value: :class:`~godafoss.fraction`
            value as a fraction of te full scale
        """
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "gf.dac":
        """
        dac that outputs the negative (complement) of the written value

        :result: :class:`~godafoss.dac`
            dac that, when written to, writes the complement of that value
            to the original dac

        This function returns a dac that outputs the negative
        (complement) of the written value to the original dac.

        examples::
        $insert_example( "test_dac.py", "dac invert examples", 2 )
        """

        return _gf._dac_inverted( self )

    # =======================================================================

# ===========================================================================


class _dac_inverted( dac ):
    """proxy that inverts a dac"""

    # =======================================================================

    def __init__( self, pin: dac ) -> None:
        self._pin = pin
        dac.__init__( self )

    # =======================================================================

    def write( self, value: gf.fraction ) -> None:
        self._pin.write( - value )

    # =======================================================================

    def inverted( self ) -> dac:
        return self._pin

    # =======================================================================

# ===========================================================================

import godafoss as gf


# ===========================================================================

class digits:
    """
    seven-segments display

    :param n: int
        the number of digits

    :param digit_order: Iterable[ int ] | None
        the number of digits

    This class abstracts a seven-segment display.

    When the digit_order is not specified, it is range( n ).

    When the digit_order is specified, it is the order in which the
    numerical digits are placed.
    When this digit_order skips some digits, those are not
    considered numeric digits, and they are not included in the
    p count, and are not used by the write() method.
    Such 'digits' can still be written by the write_digit_segments()
    method.

    The n attribute is the number of digits.
    The p ttribute is the number of numeric digits.
    The segments attribute provides the translation from value
    to active segments.
    The LSB is segment a, the MSB - 1 is segment g.
    """

    segments = {
        '0': 0b_0011_1111,
        '1': 0b_0000_0110,
        '2': 0b_0101_1011,
        '3': 0b_0100_1111,
        '4': 0b_0110_0110,
        '5': 0b_0110_1101,
        '6': 0b_0111_1101,
        '7': 0b_0000_0111,
        '8': 0b_0111_1111,
        '9': 0b_0110_1111,
        ' ': 0b_0000_0000,
        '-': 0b_0100_0000,
        '_': 0b_0000_1000,
        'h': 0b_0111_0100,
        'H': 0b_0111_0110,
        'o': 0b_0101_1100,
        'C': 0b_0110_0001,
        'c': 0b_0101_1000,
    }


    # =======================================================================

    def __init__(
        self,
        n: int,
        digit_order = None # : Iterable[ int ] = None
        # from collections.abc import Iterable
    ):
        self.n = n
        self._digit_order = \
            digit_order if digit_order is not None else list( range( n ) )
        self.p = len( self._digit_order )
        self._dirty = True

    # =======================================================================

    def write_digit_segments(
        self,
        n: int,
        v: int
    ):
        """
        write the segments of a single digit

        :param n: int
            the digit that is written

        :param v: int
            the seven-segment value

        This method writes the 8-bit value v to the segments of digit n.
        The digit order (optional constructor parameter) is NOT
        taken into account by this method.
        The LSB is written to segment a, the MSB to the decimal point.

        When n is outside the number of valid digits,
        the write_digit_segments() call has no effect.

        A segments display can be buffered, so a flush() call might be
        required to effectuate what was written by write_digit_segments()
        calls.
        """

        raise NotImplementedError

    # =======================================================================

    def write_digits(
        self,
        values # : Iterable[ int ]
    ):
        """
        write the 8-bit values to the segments of the digits

        :param values: Iterable[ int ]
            the values to write to the numeric digits

        This method writes the 8-bit values to the digits
        of the display, starting at the leftmost one.
        The digit order (optional constructor parameter) is NOT
        taken into account by this method.
        Excess values (beyond the number of numerical digits in the display)
        are ignored.
        """

        for i, s in enumerated( values ):
            write_digit_segments( i, s )

    # =======================================================================

    def flush(
        self,
        forced: bool = False
    ) -> None:
        """
        effectuate what was written to the display

        :param forced: bool
            True forces a flush, even when no changes were made

        Writes to the 7 segment display can be buffered.
        If so, a flush() method call is required to effectuate
        what was written.

        A flush() call might be a no-op when nothing was written since
        the previous flush() call, unless the forced parameter is True.
        """

        if self._dirty or forced:
            self._dirty = False
            self._flush_implementation()

    # =======================================================================

    def _flush_implementation( self ) -> None:
        """
        flush the content (concrete implementation)

        This method must be implemented by a concrete class.
        """

        raise NotImplementedError

    # =======================================================================

    def write(
        self,
        s: str,
        points = (), # : Iterable[ bool ] = (),
        align = True,
        ink: bool = True,
        flush: bool = True
    ):
        """
        write a string to the display

        This method writes the string s to the display.
        Valid characters that are the digits 0-9, the characters
        hHoCc-_ and the space.
        A point or comma enables the decimal point of the previous digit.
        Other characters are ignored.

        The valid characters and their representation in segments
        are stored in the segments attribute.
        Characters can be added or changed if desired.

        By default, the result will be written right-aligned: spaces
        (digits with no segments enabled) will be prepended to
        fill the number of digits in the display.
        When the align parameter is False, result will be
        written left-aligned (spaces will be appended instead of prepended).

        The decimal points can also be enabled by the elements
        of the points parameter.
        Each element enables the decimal point of
        one digit in the result (after alignment).

        By default, enabled segments will light up.
        When the ink parameter is False, this will  be reversed:
        non-enabled segments will light up.

        By default, the display will be updated (flush() call).
        When the flush parameter is False no flush() will be called,
        hence a flush() call might be needed to effectuate the write.

        This method takes the digit_order (optional constructor parameter)
        into account. Digits that are not present in the digit_order
        are skipped.
        """

        result = []
        for c in s:

            if c in [ ",", "." ]:
                if len( result ) > 0:
                    result[ -1 ] = result[ -1 ] | 0x80

            elif c in self.segments:
                result.append( self.segments[ c ] )

            else:
                # ignore other characters
                pass

        while len( result ) < self.p:
            if align:
                result.insert( 0, 0 )
            else:
                result.append( 0 )

        for i, point in enumerate( points ):
            if ( i < self.p ) and point:
                result[ i ] = result[ i ] | 0x80

        for i, v in enumerate( result ):
            if not ink:
                v = 0xFF ^ v
            if i < self.p:
                self.write_digit_segments( self._digit_order[ i ], v )

        if flush:
            self.flush()

    # =======================================================================

    def demo(
        self,
        *args,
        **kwargs
    ):
        """
        seven-segment display demo
        """

        from godafoss.gf_digit_demos import digits__demo

        digits_demo( self, *args, **kwargs )


# ===========================================================================

# ===========================================================================

class spi:
    """
    $$ref( "https://en.wikipedia.org/wiki/Serial_Peripheral_Interface", "spi" )
    bus

    :param sck: (int|str)
        the clock pin

    :param mosi: (int|str)
        the master-out-slave-in pin

    :param miso: (int|str)
        the master-in-slave-out pin

    :param frequency: (int)
        the (maximum) clock frequency

    :param mode: (int)
        the mode (0..3), which determines the polarity and phase;
        check clock polarity and phase in this
        $$ref( "https://en.wikipedia.org/wiki/Serial_Peripheral_Interface", "spi wiki" )

    :param implementation: (int)
        the
        $$ref( "#spi_implementation" )
        : spi_implementation.soft (default)
        or spi_implementation.hard

    :param id: (int)
        the spi channel id
        (specifying an id forces the mechansim to
        be gf.spi_implementation.hard)

    All pins must be physical pins of the target (not godafoss pin objects).
    """

    # =======================================================================

    def __init__(
        self,
        sck: int | str,
        mosi: int | str,
        miso: int | str,
        frequency: int = 10_000_000,
        mode: int = 0,
        implementation: int = gf.spi_implementation.soft,
        id: int = None
    ):

        self._sck = sck
        self._mosi = mosi
        self._miso = miso
        self._frequency = frequency
        self._mode = mode
        self._implementation = implementation

        if self.id is not None:
            self._implementation = gf.spi_implementation.hard

        if self._mode == 0:
            self._polarity, self._phase = 0, 0

        elif self._mode == 1:
            self._polarity, self._phase = 0, 1

        elif self._mode == 2:
            self._polarity, self._phase = 1, 0

        elif self._mode == 3:
            self._polarity, self._phase = 1, 1

        else:
            ValueError( "unknown spi mode {self._mode}" )

        if self._implementation == gf.spi_implementation.soft:

            import machine
            self.bus = machine.SoftSPI(
                baudrate = self._frequency,
                polarity = self._polarity,
                phase = self._phase,
                sck = self._machine.Pin( self._sck ),
                mosi = self._machine.Pin( self._mosi ),
                miso = self._machine.Pin( self._miso )
            )

        elif self._implementation == gf.spi_implementation.hard:

            import machine
            if self._id is None:

                import os
                uname = os.uname()[ 0 ]

                if uname == "rp2":
                    self._id = 0

                elif uname == "mimxrt":
                    self.bus = machine.SPI(
                        1,
                        baudrate = self._frequency,
                        polarity = self._polarity,
                        phase = self._phase
                    )
                    return

                else:
                    ValueError( "unknown system (%s), specify the id" % uname )

            self._bus = machine.SPI(
                self._id,
                baudrate = self._frequency,
                polarity = self._polarity,
                phase = self._phase,
                sck = machine.Pin( self._self.sck ),
                mosi = machine.Pin( self._self.mosi ),
                miso = machine.Pin( self._self.miso )
            )

        else:
            raise ValueError( f"unknown spi implementation {self._implementation}" )

    # =======================================================================

    def write(
        self,
        *args,
        **kwargs
    ) -> None:
        """
        write parameter(s) to the spi bus
        """

        self._bus.write(
            *args,
            **kwargs
        )

    # =======================================================================

# ===========================================================================

# ===========================================================================

class touch:
    """
    lcd touch sensor interface
    """

    # =======================================================================

    def __init__(
        self,
        span: int,
        size: gf.xy
    ):
        self._span = span
        self._size = size

    # =======================================================================

    def touch_adcs( self ):
        """
        read and return the raw x and y touch ADC values.

        :result: int, int
            tuple of the 12-bit x and y ADC values of the touch point
            None, None when no touch
        """

        raise NotImplementedError

    # =======================================================================

    def touch_fractions( self ):
        """
        read and return the x and y touch values as fractions

        :result: :class:`~godafoss.fraction`, :class:`~godafoss.fraction`
            tuple of the 12-bit x and y ADC values, or None

        This function reads the two ADC touch channels.
        When no touch is detected, None is rerurned
        When a touch is detected, a list of the x and y touch
        locations is returned as a :class:`~godafoss.fraction` pair.
        """
        a, b = self.touch_adcs()

        if a == None:
            return None

        return gf.fraction( a, self._span ), gf.fraction( b, self._span )

    # =======================================================================

    def touch_xy(
        self,
        size: gf.xy
    ):
        """
        read and return the touch location as xy pixel cooordinates

        :result: None, :class:`~godafoss.xy`
            the touch location, or None if no touch
        """
        t = self.touch_fractions()
        if t == None:
            return None
        x, y = t

        return gf.xy(
            x.scaled( 0, size.x -1 ),
            y.scaled( 0, size.y -1 )
        )

    # =======================================================================

    def demo( self ):
        """
        demo: print touch adc values
        """

        print( "touch demo" )
        while True:
            a, b = self.touch_adcs()
            if a is not None:
                print( "(%d,%d)" % ( a, b ) )
                sleep_us( 200_000 )

# ===========================================================================

