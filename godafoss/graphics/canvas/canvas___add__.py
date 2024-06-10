# ===========================================================================
#
# file     : canvas___add__.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================


class canvas___add__( gf.canvas ):

    def __init__(
        self,
        a: gf.canvas,
        b: gf.canvas
    ):
        self._a = a
        self._b = b
        gf.canvas.__init__(
            self,
            gf.xy(
                max( self._a.size.x, self._b.size.x ),
                max( self._a.size.y, self._b.size.y )
            ),
            a.is_color and b.is_color,
            a.background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ] = True
    ) -> None:
        self._a.write_pixel( location, ink )
        self._b.write_pixel( location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._a.flush( forced )
        self._b.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ gf.color | bool ] = False
    ) -> None:
        self._a.clear( ink )
        self._b.clear( ink )

    # =======================================================================

# ===========================================================================
