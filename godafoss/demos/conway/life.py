# ===========================================================================
#
# file     : life.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class life:

    """
- life itself is a canvas
- you can clear it and write to it
- you can write it to another canvas
    """

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        wraparound: bool = False
    ):
        self.canvas = canvas
        self.alive = [
            [ 0 for _ in range( size.x ) ]
            for _ in range( self.y )
        ]
        self.next = [
            [ 0 for _ in range( size.x ) ]
            for _ in range( self.y )
        ]


    # =======================================================================

    def generation( self ):
        for p in range( self.size ):
            n = 0
            for d in p.around():
                if d.within( self.size ):
                    if self.alive[ d.x ][ d.y ]:
                        n += 1
            if n < 2:
                self.next[ p.x ][ p.y ] = False
            elif n == 2:
                self.next[ p.x ][ p.y ] = self.alive[ d.x ][ d.y ]
            elif n == 3:
                self.next[ p.x ][ p.y ] = True
            else:
                self.next[ p.x ][ p.y ] = False
        temp = self.alive
        self.alive = self.next
        self.next = temp


    # =======================================================================

    def write(
        self,
        s: "sheet",
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: [ bool, gf.color ] = True
    ):
        alive = ink
        dead = not ink
        for p in self.size:
            s.write(
                p + offset,
                alive if self.alive[ p.x ][ p.y ] else dead
            )


    # =======================================================================


# ===========================================================================
