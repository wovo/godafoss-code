# ===========================================================================
#
# file     : font_default__read.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class font_default_image( gf.glyph ):
    """
    glyph of the built-in 8x8 font
    """

    def __init__( self, c ):
        gf.glyph.__init__( self, gf.xy( 8, 8 ) )

        import framebuf
        buf = bytearray(( self.size.y // 8 ) * self.size.x )
        self._charbuf = framebuf.FrameBuffer( buf, 8, 8, framebuf.MONO_VLSB )
        self._charbuf.fill( 0 )
        self._charbuf.text( c, 0, 0 )

    def read(
        self,
        location: gf.xy
    ) -> bool:
        return self._charbuf.pixel( location.x, location.y )


# ===========================================================================

def font_default__read( self, c: chr ) -> gf.glyph:
    if gf.running_micropython:
        return font_default_image( c )
    else:
        return gf.font_default_image_native( c )


# ===========================================================================

