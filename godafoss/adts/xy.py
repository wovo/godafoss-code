# ===========================================================================
#
# file     : xy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class xy( gf.immutable ):
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
        gf.immutable.__init__( self )

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
            if gf.running_micropython:
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
        return _gf.text( t ) @ self

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
