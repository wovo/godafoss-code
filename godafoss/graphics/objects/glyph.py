# ===========================================================================
#
# file     : glyph.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class glyph( gf.shape ):
    """
    rectangualar area of monochrome pixels, can be drawn to a
    :class:`~godafoss.sheet`

    :param size: :class:`~godafoss.xy`
        the size of a glyph
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
    ) -> bool:
        """
        the 'color' of the pixel at the location

        :param location: :class:`~godafoss.xy`
            the location within the glyph for which the pixel is retrieved
        """
        raise NotImplementedError

    # =======================================================================

    def write(
        self,
        sheet: "sheet",
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: bool | gf.color = True
    ) -> None:
        """
        write the glyph to the sheet

        :param sheet: :class:`~godafoss.canvas`
            the canvas to which the glyph is written

        :param offset: :class:`~godafoss.xy`
            the location within the sheet where the glyph is written
        """
        for x in range( self.size.x ):
            for y in range( self.size.y ):
                if self.read( gf.xy( x, y ) ):
                    sheet.write_pixel( offset + gf.xy( x, y ), ink )

    # =======================================================================

# ===========================================================================

