# ===========================================================================
#
# file     : circle.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class circle( gf.shape ):
    """
    circle shape

    :param radius: (int)
        the radius of the circle

    :param fill: (bool)
        whether the circle is outline (False, default) or filled (True)

    $$insert_image( "circles", 300 )

    Without any offset, a circle has its centre at the origin
    (xy(0,0), the top-left pixel of the sheet).

    $macro_insert shape
    """

    def __init__(
        self,
        radius: int,
        fill = False
    ):
        self._radius = radius
        self._fill = fill
        gf.shape.__init__( self )

    def write(
        self,
        sheet: "sheet",
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: [ bool, gf.color ] = True
    ):
        """
        write the circle to the sheet

        $macro_insert shape_write
        """

        # don't draw anything when the size would be 0
        if self._radius < 1:
            return

        # http://en.wikipedia.org/wiki/Midpoint_circle_algorithm

        fx = 1 - self._radius
        ddFx = 1
        ddFy = -2 * self._radius
        x = 0
        y = self._radius

        while x < y + 1:

            self._draw_circle_part( sheet, offset, x,  y, ink )
            self._draw_circle_part( sheet, offset, x, -y, ink )
            self._draw_circle_part( sheet, offset, y,  x, ink )
            self._draw_circle_part( sheet, offset, y, -x, ink )

            # calculate next outer circle point
            if fx >= 0:
                y -= 1
                ddFy += 2
                fx += ddFy

            x += 1
            ddFx += 2
            fx += ddFx

    def _draw_circle_part(
        self,
        sheet,
        offset,
        x,
        y,
        ink
    ):
        sheet.write_pixel( offset + gf.xy( - x, y ) )
        sheet.write_pixel( offset + gf.xy( + x, y ) )
        if self._fill:
            sheet.write(
                gf.line( 2 * gf.xy( x, 0 ) ), gf.xy( -x,  y ) + offset,
                ink
            )


# ===========================================================================
