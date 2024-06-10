# ===========================================================================
#
# file     : canvas__extended.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class canvas__extended( gf.canvas ):

    def __init__(
        self,
        one: gf.canvas,
        other: gf.canvas,
        direction: str = "EN"
    ) -> None:
        """
    extension of the canvas

    This method returns a canvas that extends the original canvas.

    The direction determines where the other canvas is placed
    relative to the original canvas (north, east, south or west),
    and which side of the canvases is aligned
    (again: north, east, south or west).
    Valid values for the direction are
    "ES", "EN", "WS", "WN", "NW", "NE", "SW", "SE".
        """

        if len( direction ) != 2:
            raise ValueError( "direction must be 2 characters" )
        direction, alignment = direction

        # which canvas comes first
        if direction in "SE":
            a, b = one, other
        elif direction in "NW":
            a, b = other, one
        else:
           raise ValueError( "direction[ 0 ] is invalid" )

        # size depends on extension direction: x or y
        # shift depends on both extension direction and alignment
        if direction in "EW":
            size = gf.xy(
                a.size.x + b.size.x,
                max( a.size.y, b.size.y ) )

            if alignment == "S":
                a_shift = gf.xy( 0,        size.y - a.size.y )
                b_shift = gf.xy( a.size.x, size.y - b.size.y )

            elif alignment == "N":
                a_shift = gf.xy( 0,        0 )
                b_shift = gf.xy( a.size.x, 0 )

            else:
                raise ValueError( "direction[ 1 ] is invalid" )

        elif direction in "NS":
            size = xy(
                max( a.size.x, b.size.x ),
                a.size.y + b.size.y )

            if alignment == "E":
                a_shift = gf.xy( b.size.x - a.size.x, 0 )
                #b_shift = xy( a.size.x, 0 )

            elif alignment == "W":
                a_shift = gf.xy( 0, 0 )
                b_shift = gf.xy( 0, a.size.y )

            else:
                raise ValueError( "direction[ 1 ] is invalid" )

        gf.canvas.__init__( self, size, a.is_color, a._background )
        self._subs = ( ( a, - a_shift ), ( b, - b_shift ) )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ]
    ) -> None:
        for canvas, offset in self._subs:
            canvas.write_pixel( location + offset, ink )

    # =======================================================================

    def _flush(
        self,
        forced: bool
    ) -> None:
        for canvas, offset in self._subs:
            canvas.flush( forced )

    # =======================================================================

# ===========================================================================
