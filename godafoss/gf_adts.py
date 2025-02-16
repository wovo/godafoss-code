# ===========================================================================
#
# file     : adts.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (godafoss.license)
#
# ===========================================================================

from godafoss import *


# ===========================================================================
#
# simple unit system
#
# ===========================================================================

def one( name: str ) -> "_one":
    return _one( { name: 1 }, 1 )

# ===========================================================================

class _one( immutable ):

    # =======================================================================

    def __init__(
        self,
        names: [ str ],
        value: any
    ) -> None:
        self.names = names
        self.value = value
        immutable.__init__( self )

    # =======================================================================

    @staticmethod
    def _make_one(
        names: [ str ],
        value: any
    ):
        if names == {}:
            return value
        else:
            return _one( names, value )

    # =======================================================================

    @staticmethod
    def _addop(
        left: "_one",
        right: any,
        operator
    ) -> "_one":
        if not isinstance( right, _one ):
            return NotImplemented

        if left.names != right.names:
            return NotImplemented

        return _one(
            left.names,
            operator( left.value, right.value )
        )

    # =======================================================================

    @staticmethod
    def _combine_names(
        left: "_one",
        right: "_one",
        operator
    ):
        result = {}
        for name, value in left.items():
            n = operator( value, right.get( name, 0 ) )
            if n != 0:
                result[ name ] = n
        for name, value in right.items():
            n = operator( left.get( name, 0 ), value )
            if n != 0:
                result[ name ] = n
        return result

    # =======================================================================

    @staticmethod
    def _mulop(
        left: "_one",
        right: any,
        names_op,
        values_op
    ) -> any:
        if isinstance( right, _one ):
            return _one._make_one(
                _one._combine_names(
                    left.names,
                    right.names,
                    names_op
                ),
                values_op( left.value, right.value )
            )

        else:
            return _one._make_one(
                left.names,
                values_op( left.value, right )
            )

    # =======================================================================

    @staticmethod
    def _compare(
        left: "_one",
        right: any,
        compare
    ) -> bool:
        if not isinstance( right, _one ):
            return NotImplemented

        if left.names != right.names:
            return NotImplemented

        return compare( left.value, right.value )

    # =======================================================================

    def __add__(
        self,
        other: any
    ) -> any:
        return _one._addop(
            self,
            other,
            lambda a, b: a + b
        )

    # =======================================================================

    def __sub__(
        self,
        other: any
    ) -> any:
        return _one._addop(
            self,
            other,
            lambda a, b: a - b
        )

    # =======================================================================

    def __mul__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a + b,
            lambda a, b: a * b
        )

    # =======================================================================

    def __rmul__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a + b,
            lambda a, b: a * b
        )

    # =======================================================================

    def __truediv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: a / b
        )

    # =======================================================================

    def __rtruediv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: b / a
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: a // b
         )

    # =======================================================================

    def __rfloordiv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: b // a
         )

    # =======================================================================

    def __eq__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a == b
        )

    # =======================================================================

    def __lt__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a < b
        )

    # =======================================================================

    def __gt__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a > b
        )

    # =======================================================================

    def __str__( self ) -> str:
        return str( self.value ) + "*" + "".join(
            f"{name}^{self.names[name]}"
                for name in sorted( self.names )
        )

    # =======================================================================


# ===========================================================================
#
# 2d coordinates
#
# ===========================================================================

class xy( immutable ):
    """
    immutable xy coordinate pair or 2d vector

    :param x: int
        x value

    :param y: int
        y value

    An xy value represents a location or displacement in a 2d integer grid.
    Such values can for instance be used for pixel or character
    cooordinates within a window.

    The x and y values, and the xy tuple are available
    as attributes.

    The supported operations are addition, subtraction, negation,
    multiplication (by an integer), integer division (by an integer),
    and taking the string representation.

    examples
    insert_example( "tests/unit_test_xy.py", "xy examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        self.x = x
        self.y = y
        self.xy = ( x, y )
        immutable.__init__( self )

    # =======================================================================

    def __iter__(
        self
    ) -> "xy":
        for y in range( self.y ):
            for x in range( self.x ):
                yield xy( x, y )

    # =======================================================================

    def around(
        self
    ) -> "xy":
        """
        generate the 8 locations around the xy value
        """
        for dy in range( -1, 0, +1 ):
            for dx in range( -1, 0, +1 ):
                if ( dx != 0 ) or ( dy != 0 ):
                    yield xy( self.x + dx, self.y + dy )

    # =======================================================================

    def within(
        self,
        boundary: "xy"
    ) -> "xy":
        """
        whether the xy value is within the boundary

        The xy value is within the boundary if both
        ( 0 <= x < boundary.x ) and ( 0 <= y < boundary.y ).
        """
        return (
            ( self.x >= 0 )
            and ( self.y >= 0 )
            and ( self.x < boundary.x )
            and ( self.y < boundary.y )
        )

    # =======================================================================

    def __eq__(
        self,
        other: "xy"
    ) -> bool:
        return ( self.x == other.x ) and ( self.y == other.y )

    # =======================================================================

    def __add__(
        self,
        other: "xy"
    ) -> "xy":
        return xy(
            self.x + other.x,
            self.y + other.y
        )

    # =======================================================================

    def __sub__(
        self,
        other: "xy"
    ) -> "xy":
        return xy(
            self.x - other.x,
            self.y - other.y
        )

    # =======================================================================

    def __neg__( self ) -> "xy":
        return xy(
           - self.x,
           - self.y
        )

    # =======================================================================

    def __mul__(
        self,
        other: any
    ) -> "xy":
        if isinstance( other, int ):
            return xy(
                self.x * other,
                self.y * other
            )
        else:
            if running_micropython:
                raise NotImplementedError
            return NotImplemented

    # =======================================================================

    def __rmul__(
        self,
        other: int
    ) -> "xy":
        return xy(
            self.x * other,
            self.y * other
        )

    # =======================================================================

    def __rmatmul__(
        self,
        t: str
    ) -> "xy":
        return _text( t ) @ self

    # =======================================================================

    def __floordiv__(
        self,
        other: int
    ) -> "xy":
        return xy(
            self.x // other,
            self.y // other
        )

    # =======================================================================

    def __repr__( self ) -> "str":
        return "(%d,%d)" % ( self.x, self.y )

    # =======================================================================


# ===========================================================================
#
# 3d coordinates
#
# ===========================================================================

class xyz( immutable ):
    """
    xyz 3d coordinates or vector

    :param x: int | float
        x value

    :param y: int | float
        y value

    :param z: int | float
        z value

    An xyz value represents a vector in a 3d space.
    Such values can for instance be used to represent the direction
    of gravity returned by an acceleration sensor.

    The x, y and z values, and the xyz tuple are available
    as attributes.

    The supported operations are addition, subtraction, negation,
    multiplication (by an integer or float), true division and floor division
    (by an integer or float), and taking the string representation.

    $macro_insert immutable

    examples
    $insert_example( "test_xyz.py", "xyz examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        x: int | float,
        y: int | float,
        z: int | float,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.xyz = ( x, y, z )
        immutable.__init__( self )

    # =======================================================================

    def __eq__(
        self,
        other: "xy"
    ) -> bool:
        return ( self.x == other.x ) \
            and ( self.y == other.y ) \
            and ( self.z == other.z )

    # =======================================================================

    def __add__(
        self,
        other: "xyz"
    ) -> "xyz":
        return xyz(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    # =======================================================================

    def __sub__(
        self,
        other: "xyz"
    ) -> "xyz":
        return xyz(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    # =======================================================================

    def __neg__( self ) -> "xyz":
        return xyz(
           - self.x,
           - self.y,
           - self.z
        )

    # =======================================================================

    def __mul__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x * other,
            self.y * other,
            self.z * other
        )

    # =======================================================================

    def __rmul__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x * other,
            self.y * other,
            self.z * other
        )

    # =======================================================================

    def __truediv__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x / other,
            self.y / other,
            self.z / other
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x // other,
            self.y // other,
            self.z // other
        )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d,%d,%d)" % ( self.x, self.y, self.z )

    # =======================================================================


# ===========================================================================
#
# RGB emissive colors
#
# ===========================================================================

class color( immutable ):
    """
    rgb color

    :param red: int
        red channel brightness (0..255)

    :param green: int
        green channel brightness (0..255)

    :param blue: int
        blue channel brightness (0..255)

    This is a (red, green, blue) color value.

    The red, green and blue attributes are in the range 0...255.
    Values outside this range are clamped to the nearest value
    within the range.
    The rgb attribute is the tuple of the read, green and blue
    attributes.

    The color channel values are additive
    (like light; not subtractive, like paint or filters).

    Two colors can be added or subtracted.

    Colors and be multiplied by an integer value,
    or divided by an integer value.

    Some common colors are available as attributes of the colors class.

    $macro_insert invertible

    $macro_insert immutable

    examples
    $insert_example( "test_color.py", "color examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        red: int,
        green: int,
        blue: int
    ) -> None:
        self.red   = clamp( red, 0, 255 )
        self.green = clamp( green, 0, 255 )
        self.blue  = clamp( blue, 0, 255 )
        immutable.__init__( self )

    # =======================================================================

    def rgb( self ):
        """
        return the 3 values read, green, blue
        """
        return self.red, self.green, self.blue

    # =======================================================================

    def __hash__( self ) -> int:
        return ( self.red << 16 ) + ( self.green << 8 ) + self.blue

    # =======================================================================

    def __eq__(
        self,
        other: "xy"
    ) -> bool:
        return ( self.red == other.red ) \
            and ( self.green == other.green ) \
            and ( self.blue == other.blue )

    # =======================================================================

    def __add__(
        self,
        other: "color"
    ) -> "color":
        return color(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue
        )

    # =======================================================================

    def __sub__(
        self,
        other: "color"
    ) -> "color":
        return color(
            self.red - other.red,
            self.green - other.green,
            self.blue - other.blue
        )

    # =======================================================================

    def inverted( self ) -> "color":
        """
        the complement of the color

        A color can be negated, which yields the complimentary
        :class:`~godafoss.color`.

        examples::
        $insert_example( "test_color.py", "color invert example", 2 )
        """
        return color( 0xFF, 0xFF, 0xFF ) - self

    # =======================================================================

    def __neg__( self ) -> "color":
        return color( 0xFF, 0xFF, 0xFF ) - self

    # =======================================================================

    def __mul__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red * other,
            self.green * other,
            self.blue * other
        )

    # =======================================================================

    def __rmul__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red * other,
            self.green * other,
            self.blue * other
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red // other,
            self.green // other,
            self.blue // other
        )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d,%d,%d)" % ( self.red, self.green, self.blue )

    # =======================================================================


# ===========================================================================

class colors:
    """
    some common color values
    """

    black   = color(    0,    0,    0 )
    white   = color( 0xFF, 0xFF, 0xFF )
    gray    = color( 0x80, 0x80, 0x80 )

    red     = color( 0xFF,    0,    0 )
    green   = color(    0, 0xFF,    0 )
    blue    = color(    0,    0, 0xFF )

    yellow  = color( 0xFF, 0xFF,    0 )
    cyan    = color(    0, 0xFF, 0xFF )
    magenta = color( 0xFF,    0, 0xFF )

    violet  = color( 0xEE, 0x82, 0xEE )
    sienna  = color( 0xA0, 0x52, 0x2D )
    purple  = color( 0x80, 0x00, 0x80 )
    pink    = color( 0xFF, 0xC8, 0xCB )
    silver  = color( 0xC0, 0xC0, 0xC0 )
    brown   = color( 0xA5, 0x2A, 0x2A )
    salmon  = color( 0xFA, 0x80, 0x72 )


# ===========================================================================
#
# fraction (percentage) of a whole
#
# ===========================================================================

class fraction( immutable ):
    """
    a fractional value

    :param value: int
        the value, interpreted as a fraction of the maximum

    :param maximum: int
        the value is interpreted on the scale [0..maximum]

    A fraction is conceptually a value in the range 0.0 ... 1.0.
    It is stored as a maximum (must be >0) and a value
    (will be 0 ... maximum).

    A fraction represents for instance the result of an ADC reading
    (like 512 out of 1023 for a 10-bit ADC for half the maximum voltage),
    or a setpoint for a servo
    (100 out of 400 would be 1/4 of full travel).

    The value and maximum are available as attributes.
    The scaled method returns the fraction of the interval (minimum
    and maximum).

    The inverse of a fraction inverse is the complement of its value.

    A fraction can be converted to a string representation.

    $macro_insert immutable

    examples
    $insert_example( "test_fraction.py", "fraction examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        value: int,
        maximum: int
    ):
        self.value = clamp( value, 0, maximum )
        self.maximum = maximum
        self.value_maximum = ( self.value, self.maximum )
        immutable.__init__( self )

    # =======================================================================

    def scaled(
        self,
        minimum: int | float,
        maximum: int | float
    ) -> int | float:
        """
        the fraction, scaled to an interval

        :param minimum: int | float
            the real part (default 0.0)

        :param maximum: int | float
            the imaginary part (default 0.0)

        :result: int | float
            the franctional value,
            scaled to the interval [minimum...maximum]

        The scaled method is usefull to scale a fraction to an
        interval, which is specified by the minimum and maximum parameters.
        When those parameters are integers, the result will be an integer.
        When one or both are floats, the result is a float.

        examples
        $insert_example( "test_fraction.py", "fraction scaled examples", 2 )
        """

        span = ( maximum - minimum )
        if isinstance( maximum, int ) and isinstance( minimum, int ):
            return minimum + span * self.value // self.maximum
        else:
            return minimum + span * self.value / self.maximum

    # =======================================================================

    def inverted( self ) -> "fraction":
        """
        complement of the fraction

        The inverted (negative) of a fraction is its complement.
        For instance, the complement of 3-out-of-10 is 7-out-of-10.

        examples
        $insert_example( "test_fraction.py", "fraction invert examples", 2 )
        """

        return fraction( self.maximum - self.value, self.maximum )

    # =======================================================================

    def __neg__( self ) -> "fraction":
        return fraction( self.maximum - self.value, self.maximum )

    # =======================================================================

    def __eq__( self, other ) -> bool:
        return ( self.maximum == other.maximum ) \
            and ( self.value == other.value )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d/%d)" % ( self.value, self.maximum )

    # =======================================================================


# ===========================================================================
#
# temperature with C/F/K convetsion
#
# ===========================================================================

class temperature( immutable ):
    """
    a temperature

    :param temp: int | float
        the temperaturee, interpreted according to the scale

    :param scale: int
        the scale

    This class holds a temperature as a float.
    When constructing a temperature, or retrieveing value
    from a temperature object,
    the scale (temperature.scale.Celcius, temperature.scale.Farenheit
    or temperature.scale.Kelvin) must be specified.

    $macro_insert immutable

    examples::
    $insert_example( "test_temperature.py", "temperature examples", 1 )
    """

    class scale:
        kelvin     = "K"
        celcius    = "C"
        farenheit  = "F"

    def __init__(
        self,
        temp: int | float,
        scale: int
    ) -> None:
        self._scale = scale

        if self._scale == self.scale.kelvin:
            self._kelvin = float( temp )

        elif self._scale == self.scale.celcius:
            self._kelvin = temp + 273.15

        elif self._scale == self.scale.farenheit:
            self._kelvin = ( temp + 459.67 ) * 5 / 9

        else:
            raise ValueError

        immutable.__init__( self )

    # =======================================================================

    def value(
        self,
        scale: chr
    ) -> float:
        """
        the temperature in the specified scale

        :param scale: chr
            the scale

        :result: float
            the temperature, excressed in the specified scale

        The temperature is return according to the specified scale,
        which must be one of temperature.scale.Celcius,
        temperature.scale.Farenheit or temperature.scale.Kelvin.

        This method returns the temperature in the requested scale.
        """

        if scale == self.scale.kelvin:
            return self._kelvin

        elif scale == self.scale.celcius:
            return self._kelvin - 273.15

        elif scale == self.scale.farenheit:
            return 1.8 * ( self._kelvin - 273.15) + 32

        else:
            raise ValueError

    # =======================================================================

    def __repr__( self ) -> str:
        return "%f%s" % (
            self.value( self._scale ),
            self._scale
        )
    # =======================================================================

# ===========================================================================
