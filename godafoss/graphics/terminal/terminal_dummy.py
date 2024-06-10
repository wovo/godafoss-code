# ===========================================================================
#
# file     : terminal_dummy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class terminal_dummy( gf.terminal ):

    # =======================================================================

    def __init__(
        self,
        size: gf.xy
    ) -> None:
        gf.terminal.__init__( self, size )
        self._lines = list(
            [ "*" for x in range( self.size.x ) ]
            for y in range( self.size.y )
        )
        self.last_cursor = self.cursor

    # =======================================================================

    def _write_implementation(
        self,
        c: chr
    ) -> None:
        self._lines[ self.cursor.y ][ self.cursor.x ] = c

    # =======================================================================

    def lines( self ) -> [ str ]:
        return [
            "".join( self._lines[ y ] )
            for y in range( self.size.y )
        ]

# ===========================================================================
