# ===========================================================================
#
# file     : canvas__folded.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class canvas__folded( gf.canvas ):

    def __init__(
        self,
        subject: gf.canvas,
        n: int,
        zigzag: bool
    ) -> None:
        self._subject = subject
        self._n = n
        self._zigzag = zigzag
        canvas.__init__(
            self,
            gf.xy( subject.size.x // n, subject.size.y * n ),
            is_color = subject.is_color,
            background = subject.background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, gf.color ]
    ) -> None:
        x, y = location.x, location.y
        if self._zigzag and ( ( y % 2 ) == 1 ):
            x = self.size.x - ( x + 1 )
        x = x + self.size.x * ( y // self._subject.size.y )
        y = y % self._subject.size.y
        self._subject.write_pixel( gf.xy( x, y ), ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ bool, gf. color ]
    ) -> None:
        self._subject.clear( ink )

    # =======================================================================

# ===========================================================================
