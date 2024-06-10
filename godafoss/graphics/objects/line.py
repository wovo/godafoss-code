# ===========================================================================
#
# file     : line.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class line( gf.shape ):
    """
    line shape

    :param span: (:class:`godafoss.xy`)
        the far end of the line, as offset from the start

    $$insert_image( "lines", 300 )

    Without any offset, a line starts at the origin
    (xy(0,0), the top-left pixel of the sheet).

    $macro_insert shape
    """

    def __init__(
        self,
        span: gf.xy
    ):
        self._span = span
        gf.shape.__init__( self )

    def write(
        self,
        s: "sheet",
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: [ bool, gf.color ] = True
    ):
        """
        write the line to the sheet

        $macro_insert shape_write
        """

        x0 = offset.x
        y0 = offset.y
        x1 = offset.x + self._span.x
        y1 = offset.y + self._span.y

        # http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        # http://homepages.enterprise.net/murphy/thickline/index.html

        steep = abs( y1 - y0 ) >= abs( x1 - x0 )
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        dx = x1 - x0
        dy = y1 - y0

        xstep = 1
        if dx < 0:
            xstep = -1
            dx = -dx

        ystep = 1
        if dy < 0:
            ystep = -1
            dy = -dy

        Dx = dx
        Dy = dy

        TwoDy = 2 * Dy
        TwoDyTwoDx = TwoDy - 2 * Dx  # 2*Dy - 2*Dx
        E = TwoDy - Dx  # 2*Dy - Dx
        y = y0

        for x in range( x0, x1, xstep ):

            s.write_pixel(
                gf.xy( y, x ) if steep else gf.xy( x, y ),
                ink
            )

            if E > 0:
                E += TwoDyTwoDx  # E += 2*Dy - 2*Dx
                y = y + ystep
            else:
                E += TwoDy  # E += 2*Dy


# ===========================================================================
