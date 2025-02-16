# ===========================================================================
#
# file     : canvas_shapes.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from godafoss import *


# ===========================================================================

class shape:
    """
    something that can be drawn on a canvas

    A shape is something that can be drawn on a :class:`~godafoss.canvas`.
    Examples are a
    :class:`~godafoss.line`,
    :class:`~godafoss.rectangle`,
    :class:`~godafoss.circle`, and
    :class:`~godafoss.glyph` (character).

    Shapes can be grouped together by adding them together
    (+ operator).
    The result is a :class:`~godafoss.shape` that, when written,
    writes all its constituent shapes.

    A shape can be pre-multiplied by an xy value, which adds
    an offset to where the shape is written.

    $macro_start shape
    This class implements the :class:`~shape` interface:
    it can be written to a :class:`~godafoss.sheet`, added to another
    :class:`~godafoss.shape`
    to form a compound shape, or post-mathmultiplied
    (@ operator) with an :class:`~godafoss.xy` value to include an offset.
    $macro_end
    """

    # =======================================================================

    def __init__(
        self
    ):
        pass

    # =======================================================================

    #def write(
    #    self,
    #    sheet: "sheet",
    #    offset: xy = xy( 0, 0 ),
    #    ink: bool | color = True
    #) -> None:
        """
        write the shape to a sheet

        :param sheet: (:class:`~godafoss.sheet`)
            the :class:`~godafoss.sheet` on which the shape must be written

        :param offset: (:class:`~godafoss.xy`, default (0,0) )
            the offset at which the shape must be written

        Writing a :class:`~godafoss.shape` is additive
        in the sense that pixels that are True
        are written in the sheets foreground 'color', while pixels that
        are False are not written.

        $macro_start shape_write
        :param sheet: (:class:`~godafoss.sheet`)
            the :class:`~godafoss.sheet` on which the shape must be written

        :param offset: (:class:`~godafoss.xy`, default (0,0) )
            the offset at which the shape must be written

        Writing a :class:`~godafoss.shape` is additive in the sense
        that pixels that are True are written in the sheets
        foreground 'color', while pixels that are False are not written.
        $macro_end
        """

     #   raise NotImplementedError

    # =======================================================================

    def __add__(
        self,
        other: "shape"
    ) -> "shape":
        return _shape_add( self, other )

    # =======================================================================

    def __rmatmul__(
        self,
        modifier: xy
    ) -> "shape":

        #if isinstance( modifier, xy ):
            return _shape_offset( self, modifier )

        # color -> image
        # sequence of modifiers -> apply all (mustb be a type??)

        #return NotImplemented


    # =======================================================================

    def __matmul__(
        self,
        modifier: xy
    ) -> "shape":

    #    if isinstance( modifier, xy ):
            return _shape_offset( self, modifier )

        # color -> image
        # sequence of modifiers -> apply all (mustb be a type??)

    #    return NotImplemented


# ===========================================================================

class _shape_offset( shape ):

    # =======================================================================

    def __init__( self, subject, offset ):
        self._subject = subject
        self._offset = offset
        shape.__init__( self )

    # =======================================================================

    def write(
        self,
        sheet: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        self._subject.write( sheet, self._offset + offset, ink )

    # =======================================================================


# ===========================================================================

class _shape_add( shape ):

    def __init__( self, a, b ):
        self._a = a
        self._b = b
        shape.__init__( self )

    def write(
        self,
        sheet: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        self._a.write( sheet, offset, ink )
        self._b.write( sheet, offset, ink )


# ===========================================================================
#
# shapes
#
# ===========================================================================

class line( shape ):
    """
    line shape

    :param span: (:class:`godafoss.xy`)
        the far end of the line, as offset from the start

    $$insert_image( "lines", 300 )

    Without any offset, a line starts at the origin
    (xy(0,0), the top-left pixel of the sheet).

    $macro_insert shape
    """

    # =======================================================================

    def __init__(
        self,
        span: xy
    ):
        self._span = span
        shape.__init__( self )

    # =======================================================================

    def write(
        self,
        s: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: [ bool, color ] = True
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
                xy( y, x ) if steep else xy( x, y ),
                ink
            )

            if E > 0:
                E += TwoDyTwoDx  # E += 2*Dy - 2*Dx
                y = y + ystep
            else:
                E += TwoDy  # E += 2*Dy

    # =======================================================================


# ===========================================================================

class rectangle( shape ):
    """
    rectangle shape

    :param span: (:class:`godafoss.xy`)
        the far end of the rectangle, as offset from the start

    $$insert_image( "rectangles", 300 )

    Without any offset, a rectangle starts at the origin
    (xy(0,0), the top-left pixel of the sheet).

    $macro_insert shape
    """

    # =======================================================================

    def __init__(
        self,
        span: xy,
        fill = False
    ):
        self._span = span
        self._fill = fill
        shape.__init__( self )

    # =======================================================================

    def write(
        self,
        s: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: [ bool, color ] = True
    ):
        """
        write the rectangle to the sheet

        $macro_insert shape_write
        """

        if self._fill:
            for dx in range( 0, self._span.x ):
                for dy in range( 0, self._span.y ):
                    s.write_pixel( offset + xy( dx, dy ), ink )
        else:
            h = line( xy( self._span.x, 0 ) )
            v = line( xy( 0, self._span.y ) )
            h.write( s, offset,                                       ink )
            h.write( s, offset + xy( 0, less( self._span.y ) ), ink )
            v.write( s, offset,                                       ink )
            v.write( s, offset + xy( less( self._span.x ), 0 ), ink )

    # =======================================================================


# ===========================================================================

class circle( shape ):
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

    # =======================================================================

    def __init__(
        self,
        radius: int,
        fill = False
    ):
        self._radius = radius
        self._fill = fill
        shape.__init__( self )

    # =======================================================================

    def write(
        self,
        sheet: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: [ bool, color ] = True
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

    # =======================================================================

    def _draw_circle_part(
        self,
        sheet,
        offset,
        x,
        y,
        ink
    ):
        sheet.write_pixel( offset + xy( - x, y ) )
        sheet.write_pixel( offset + xy( + x, y ) )
        if self._fill:
            sheet.write(
                line( 2 * xy( x, 0 ) ), xy( -x,  y ) + offset,
                ink
            )

    # =======================================================================


# ===========================================================================

class image( shape ):
    """
    a rectangualar area of colored pixels
    """

    # =======================================================================

    def __init__(
        self,
        size: xy
    ) -> None:
        self.size = size
        shape.__init__( self )

    # =======================================================================

    def read(
        self,
        location: xy

    ) -> color:
        """the color of the pixel at the location"""
        raise NotImplementedError

    # =======================================================================

    def draw_implementation(
        self,
        canvas: canvas,
        offset: xy,
        ink: [ color, bool ]
    ):
        for x in range( self.size.x ):
            for y in range( self.size.y ):
                source = xy( x, y )
                c =  self.read( source )
                canvas.draw( source + offset, c )

    # =======================================================================


# ===========================================================================

class glyph( shape ):
    """
    rectangualar area of monochrome pixels, can be drawn to a
    :class:`~godafoss.sheet`

    :param size: :class:`~godafoss.xy`
        the size of a glyph
    """

    # =======================================================================

    def __init__(
        self,
        size: xy
    ) -> None:
        self.size = size
        shape.__init__( self )

    # =======================================================================

    def read(
        self,
        location: xy
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
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
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
                if self.read( xy( x, y ) ):
                    sheet.write_pixel( offset + xy( x, y ), ink )

    # =======================================================================


# ===========================================================================

class text( shape ):

    # =======================================================================

    def __init__(
        self,
        text: str,
        font: "font" = None
    ):
        self._text = text
        self._font = font
        if self._font == None:
            # avoid draging in font_default.read()
            self._font = font_default()
            self.size = xy( len( self._text ) * 8, 8 )
        else:
            self.size = xy(
                sum( [ self._font.read( c ).size.x for c in text ] ),
                self._font.size.y
            )
        shape.__init__( self )

    # =======================================================================

    def write(
        self,
        sheet,
        offset: xy = xy( 0, 0 ),
        ink: [ color, bool, None ] = True
    ):
        x_offset_in_text = 0
        y_offset = 0
        for c in self._text:

            if c == '\n':
                x_offset_in_text = 0
                y_offset += self._font.size.y

                # quit when below the sheet
                if y_offset >= sheet.size.y:
                    return

                continue

            glyph = self._font.read( c )
            x_offset_in_sheet = offset.x + x_offset_in_text

            # skip when beyond the right side of the sheet
            if (
                # skip when before the left side of the sheet
                ( x_offset_in_sheet + glyph.size.x >= 0 )

                # skip when beyond the right side of the sheet
                and ( x_offset_in_sheet < sheet.size.x )
            ):
                glyph.write(
                    sheet,
                    offset + xy( x_offset_in_text, y_offset ),
                    ink
                )

            x_offset_in_text += glyph.size.x

    # =======================================================================


# ===========================================================================

class ggf( shape ):
    """
    read a shape from a ggf file

    :param: file_name: str
        file that contains the image data in ggf format

    :param: cached: bool
        whether the file content is read into RAM at construction
        (default: False)

    This is a shape object that is read from a ggf format file stored
    on the target.
    By default, the file content is read into RAM when the ggf object is
    constructed.
    When cached is False, the file data is read (but not permanently stored)
    when the ggf object is written to a canvas. This is slower, but
    saves RAM.

    The Godafoss Graphic Format (ggf) is a very simple uncompressed
    graphic file format.
    The gpy script (in the make directory of the godafoss github)
    can be used to create ggf files from any graphic format readable
    by PIL.

    +----------------------------------------------------------------+
    | ggf format                                                     |
    +-----------+----------------+-----------------------------------+
    | byte 0    | identification | 0xA6                              |
    +-----------+----------------+-----------------------------------+
    | byte 1    | pixel format:  | 0: 1 bit/pixel MSB first          |
    |           |                +-----------------------------------+
    |           |                | 1: 1-byte RGB 3,3,2 R first       |
    |           |                +-----------------------------------+
    |           |                | 2: 3-byte RGB R first             |
    +-----------+----------------+-----------------------------------+
    | bytes 2-3 | x pixels size  | high byte first                   |
    +-----------+----------------+-----------------------------------+
    | bytes 4-5 | y pixels size  | high byte first                   |
    +-----------+----------------+-----------------------------------+
    | bytes 6.. | pixel data     | by row; for B/W the last byte of  |
    |           |                | each row is padded to a full byte |
    +-----------+----------------+-----------------------------------+
    """

    # =======================================================================

    def __init__(
        self,
        file_name: str,
        cached: bool = True
    ) -> None:

        shape.__init__( self )

        if not file_name.endswith( ".ggf" ):
            file_name += ".ggf"
        f = open( file_name, "rb" )

        x = f.read( 1 )[ 0 ]
        if x != 0xA6:
            raise valueError(
                "file %s first byte %02X, should be 0xA6"
                % ( file_name, x ) )

        self.depth = f.read( 1 )[ 0 ]
        if not self.depth in [ 0, 1, 2 ]:
            raise ValueError(
                "file %s depth byte %d, should be 0,1,2"
                % ( file_name, depth ) )

        s = f.read( 2 )
        x = s[ 0 ] * 256 + s[ 1 ]
        s = f.read( 2 )
        y = s[ 0 ] * 256 + s[ 1 ]
        self.size = xy( x, y )

        if cached:
            self.data = f.read( x * y * 3 )
            self.write = self._write_cached
        else:
            self.file_name = file_name
            self.write = self._write_from_file

        f.close()

    # =======================================================================

    def _write_cached(
        self,
        c: canvas,
        offset: xy = xy( 0, 0 )
    ):
        i = 0
        for y in range( self.size.y ):
            for x in range( self.size.x ):

                if self.depth == 0:
                    if ( x % 8 ) == 0:
                        v = self.data[ i ]
                        i += 1
                    c.write_pixel(
                        offset + xy( x, y ),
                        v & 0x01 != 0x00
                    )
                    v = v >> 1

                elif self.depth == 1:
                    d = f.read( 1 )[ 0 ]
                    r = (( d >> 5 ) & 0x07 ) << 5
                    g = (( d >> 2 ) & 0x07 ) << 5
                    b = (( d >> 0 ) & 0x03 ) << 6
                    c.write_pixel(
                        offset + xy( x, y ),
                        color( r, g, b )
                    )

                else:
                    p = color(
                        self.data[ i ],
                        self.data[ i + 1 ],
                        self.data[ i + 2 ]
                    )
                    i += 3
                    c.write_pixel( offset + xy( x, y ), p )

    # =======================================================================

    def _write_from_file(
        self,
        c: canvas,
        offset: xy = xy( 0, 0 )
    ):
        f = open( self.file_name, "rb" )
        f.read( 5 )
        for y in range( self.size.y ):
            for x in range( self.size.x ):

                if self.depth == 0:
                    if ( x % 8 ) == 0:
                        v = f.read( 1 )[ 0 ]
                    c.write_pixel(
                        offset + xy( x, y ),
                        v & 0x01 != 0x00
                    )
                    v = v >> 1

                elif self.depth == 1:
                    d = f.read( 1 )[ 0 ]
                    r = (( d >> 5 ) & 0x07 ) << 5
                    g = (( d >> 2 ) & 0x07 ) << 5
                    b = (( d >> 0 ) & 0x03 ) << 6
                    c.write_pixel(
                        offset + xy( x, y ),
                        color( r, g, b )
                    )

                else:
                    d = f.read( 3 )
                    p = color(
                        d[ 0 ],
                        d[ 1 ],
                        d[ 2 ]
                    )
                    c.write_pixel(
                        offset + xy( x, y ),
                        p
                    )
        f.close()

    # =======================================================================


# ===========================================================================

