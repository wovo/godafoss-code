# ===========================================================================
#
# file     : canvas__combine.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================


class canvas__combine( gf.canvas ):

    def __init__(
        self,
        *args
    ):
        self._list = args
        gf.canvas.__init__(
            self,
            gf.xy(
                max( a.size.x for a in self._list ),
                max( a.size.y for a in self._list )
            ),
            all( a.is_color for a in self._list ),
            self._list[ 0 ]._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ] = True
    ) -> None:
        for x in self._list:
            x.write_pixel( location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        for x in self._list:
            x.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ gf.color | bool ] = False
    ) -> None:
        for x in self._list:
            x.clear( ink )

    # =======================================================================

# ===========================================================================
