# ===========================================================================
#
# file     : canvas_native.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

import PIL
from PIL import Image
import graphics


# ===========================================================================

class canvas_native( gf.canvas ):

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        is_color: bool = True,
        background: [ bool | gf.color ] = gf.colors.white,
        name = "godafoss",
        scale = gf.xy( 1, 1 )
    ):
        gf.canvas.__init__( self, size, is_color, background )
        self._scale = scale

        self.image = PIL.Image.new(
            "RGB",
            ( scale.x * size.x, scale.y * size.y  )
        )
        self.pixels = self.image.load()

        self.window = graphics.GraphWin(
            name,
            scale.x * size.x,
            scale.y * size.y,
            autoflush = False
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location,
        ink
    ):
        for x in range( self._scale.x ):
            for y in range( self._scale.y ):

                self.pixels[
                    self._scale.x * location.x + x,
                    self._scale.y * location.y + y
                ] = ( ink.red, ink.green, ink.blue )

                self.window.plot(
                    self._scale.x * location.x + x,
                    self._scale.y * location.y + y,
                    graphics.color_rgb( ink.red, ink.green, ink.blue )
                )


    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self.window.update()

    # =======================================================================

    def save(
        self,
        file_name: str
    ):
        self.image.save( file_name )

    # =======================================================================


# ===========================================================================
