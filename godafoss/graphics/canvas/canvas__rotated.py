# ===========================================================================
#
# file     : canvas__rotated.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def canvas__rotated(
    self,
    rotation: int
) -> gf.canvas:

    """
        rotated version of the canvas

        This method returns a canvas that is
        a rotated version of the original canvas.
        Allowed rotation values are 0, 90, 180 and 270.
    """

    if rotation == 0:
        return gf.canvas__transformed(
            self,
            self.size,
            lambda c: xy( c.x, c.y )
        )

    elif rotation == 90:
        return gf.canvas__transformed(
            self,
            gf.xy( self.size.y, self.size.x ),
            lambda c: gf.xy( self.size.x - 1 - c.y, c.x )
        )

    elif rotation == 180:
        return gf.canvas__transformed(
            self,
            self.size,
            lambda c: gf.xy( self.size.x - 1 - c.x, self.size.y - 1 - c.y )
        )

    elif rotation == 270:
        return gf.canvas__transformed(
            self,
            gf.xy( self.size.y, self.size.x ),
            lambda c: gf.xy( c.y, self.size.y - 1 - c.x )
        )

    else:
        raise ValueError( "rotation must be 0, 90, 180 or 270" )

# ===========================================================================
