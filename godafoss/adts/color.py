# ===========================================================================
#
# file     : color.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class color( gf.immutable ):
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
        self.red   = gf.clamp( red, 0, 255 )
        self.green = gf.clamp( green, 0, 255 )
        self.blue  = gf.clamp( blue, 0, 255 )
        gf.immutable.__init__( self )

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
