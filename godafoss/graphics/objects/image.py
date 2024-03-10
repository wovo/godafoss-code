# ===========================================================================
#
# file     : image.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class image( gf.shape ):
    """
    a rectangualar area of colored pixels
    """

    # =======================================================================

    def __init__(
        self,
        size: gf.xy
    ) -> None:
        self.size = size
        gf.shape.__init__( self )

    # =======================================================================

    def read(
        self,
        location: gf.xy

    ) -> gf.color:
        """the color of the pixel at the location"""
        raise NotImplementedError

    # =======================================================================

    def draw_implementation(
        self,
        canvas: gf.canvas,
        offset: gf.xy,
        ink: [ gf.color, bool ]
    ):
        for x in range( self.size.x ):
            for y in range( self.size.y ):
                source = gf.xy( x, y )
                c =  self.read( source )
                canvas.draw( source + offset, c )


# ===========================================================================

