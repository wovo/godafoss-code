# ===========================================================================
#
# file     : rectangle.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class rectangle( gf.shape ):
    """
    rectangle shape

    :param span: (:class:`godafoss.xy`)
        the far end of the rectangle, as offset from the start

    $$insert_image( "rectangles", 300 )

    Without any offset, a rectangle starts at the origin
    (xy(0,0), the top-left pixel of the sheet).

    $macro_insert shape
    """

    def __init__(
        self,
        span: gf.xy,
        fill = False
    ):
        self._span = span
        self._fill = fill
        gf.shape.__init__( self )

    def write(
        self,
        s: "sheet",
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: [ bool, gf.color ] = True
    ):
        """
        write the rectangle to the sheet

        $macro_insert shape_write
        """

        if self._fill:
            for dx in range( 0, self._span.x ):
                for dy in range( 0, self._span.y ):
                    s.write_pixel( offset + gf.xy( dx, dy ), ink )
        else:
            h = gf.line( gf.xy( self._span.x, 0 ) )
            v = gf.line( gf.xy( 0, self._span.y ) )
            h.write( s, offset,                                       ink )
            h.write( s, offset + gf.xy( 0, gf.less( self._span.y ) ), ink )
            v.write( s, offset,                                       ink )
            v.write( s, offset + gf.xy( gf.less( self._span.x ), 0 ), ink )


# ===========================================================================
