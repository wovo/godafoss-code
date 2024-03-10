# ===========================================================================
#
# file     : canvas_dummy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class canvas_dummy( gf.canvas ):

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        is_color: bool = True,
        background: [ bool | gf.color ] = gf.colors.white,
        palet = {
            gf.colors.white: '.',
            gf.colors.black: '*',
        }
    ):
        gf.canvas.__init__( self, size, is_color, background )
        self._palet = palet
        self._lines = list(
            [ "*" for x in range( self.size.x ) ]
            for y in range( self.size.y )
        )
        self.flush_count = 0

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location,
        ink
    ):
        self._lines[ location.y ][ location.x ] = \
            self._palet[ ink ]

    # =======================================================================

    def lines( self ) -> [ str ]:
        return [
            "".join( self._lines[ y ] )
            for y in range( self.size.y )
        ]

    # =======================================================================

    def __str__( self ) -> [ str ]:
        return "".join( [
            ( '        "' + "".join( self._lines[ y ] ) + '",\n' )
                for y in range( self.size.y ) ] )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self.flush_count += 1

    # =======================================================================

# ===========================================================================
