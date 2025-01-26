# ===========================================================================
#
# file     : canvas.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
from random import randint

# ===========================================================================

class canvas:
    """
    graphic drawing area, either monochrome or color

    :param location: :class:`~godafoss.xy`
        the size of the canvas in pixels in x and y direction

    :param is_color: bool
        False for a monochrome canvas, True for a color canvas

    $insert_image( "canvas-coordinates", 1, 500 )

    A canvas is a rectanglular area of either monochrome or color pixels.
    A canvas has a size attribute, which is the number of pixels in
    the x and y directions.
    The top-left pixel is at xy( 0, 0 ), the bottom-right pixel is
    at xy(canvas.size.x - i, canvas.size.y - 1).

    The is_color attribute is False for a monochrome
    canvas, or True for a color canvas.

    The write_pixel method writes a single pixel.

    The write method writes a :class:`~godafoss.shape`.

    Canvases can be added, which creates a canvas that writes
    to both constituent canvases.

    $macro_start canvas_monochrome
    This class implements the monochrome
    :class:`~godafoss.canvas` interface,
    which provides functionality to write shapes
    (:class:`~godafoss.line`, :class:`~godafoss.circle`,
    :class:`~godafoss.rectangle`, :class:`~godafoss.text`),
    to derive modified canvases
    (inverted, mirrored, rotated, parts, combinations, etc.),
    and a comprehensive demo.
    $macro_end

    $macro_start canvas_color
    This class implements the color :class:`~godafoss.canvas` interface,
    which provides functionality to write shapes
    (:class:`~godafoss.line`, :class:`~godafoss.circle`,
    :class:`~godafoss.rectangle`, :class:`~godafoss.text`),
    to derive modified canvases
    (inverted, mirrored, rotated, parts, combinations, etc.),
    and a comprehensive demo.
    $macro_end
    """

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        is_color: bool,
        background: [ bool, gf.color ]
    ):
        self.size = size
        self.is_color = is_color
        self._background = background
        self._foreground = - background if self.is_color else not background
        self._dirty = True

    # =======================================================================

    def within(
        self,
        location: gf.xy
    ):
        """
        check if the location is within the canvas

        :param location: :class:`~godafoss.xy`
            the location coordinates to be checked

        This method returns True iff the location
        is within the canvas.
        """

        return (
            gf.within( location.x, 0, self.size.x - 1 )
            and gf.within( location.y, 0, self.size.y - 1 ) )

    # =======================================================================

    def _cure_ink(
        self,
        ink: [ gf.color | bool | None ]
    ) -> [ gf.color | bool | None ]:
        """
        return specific ink

        This method returns a concrete ink:

        - None when no pixel write must be done
        - else, for a monochrome canvas: True
        - else (for a color canvas) a color
        """
        if ink is not None:
            if self.is_color:
                if isinstance( ink, bool ):
                    if ink:
                        ink = self._foreground
                    else:
                        ink = self._background
            else:
                if not isinstance( ink, bool ):
                   raise ValueError(
                       "monochrome canvas method called with color ink"
                   )
        return ink


    # =======================================================================

    def write_pixel(
        self,
        location: gf.xy,
        ink: [ gf.color | bool | None ] = True
    ) -> None:
        """
        write a pixel

        :param location: :class:`~godafoss.xy`
            the location of the pixel that is to be written

        :param ink: (:class:`~godafoss.color`, bool, None, default: True)
            the value to be written to the pixel

        This method writes a single pixel.
        When the location is within the canvas,
        and the ink parameter is not None,
        the ink is written to the pixel.

        If the ink argument is None, the pixel is not is written.

        For a monochrome canvas, the ink must (if not None)
        be a bool. When True, the foreground 'color'
        is written. When False, the pixel is not written.

        For a monochrome canvas, when the ink is a color,
        that color is written to the pixel.
        When the ink is a bool, the canvas foreground
        color is written. When False, the pixel is not written.

        A canvas can be buffered, in which case the writing of pixels is
        be effectuated only when the flush() method is called.
        """

        if ( ink is not None ) and self.within( location ):
            ink = self._cure_ink( ink )
            self._dirty = True
            self._write_pixel_implementation(
                location,
                ink
            )

    # =======================================================================

    def flush(
        self,
        forced: bool = False
    ) -> None:
        """
        effectuate what was written to the canvas

        :param forced: bool
            True forces a flush, even when no pixels were written

        Writes to the canvas can be buffered.
        If so, a flush() method call is required to effectuate
        the write_pixel() calls.

        A flush() call might be a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.

        $macro_start canvas_flush
        effectuate what was written

        :param forced: bool
            True forces a flush, even when no pixels were written

        Writes to the display are buffered:
        a flush() method call is required to effectuate what was written.

        A flush() call is a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.
        $macro_end
        """

        if self._dirty or forced:
            self._dirty = False
            self._flush_implementation( forced )

    # =======================================================================

    def write(
        self,
        thing, # : Any[ "gf.shape" | str ],
        location: gf.xy = gf.xy( 0, 0 ),
        ink: [ gf.color | None ] = None
    ):
        """
        write a :class:`~godafoss.shape` or string

        When the thing is a :class:`~godafoss.shape` the write()
        method calls the write() method of the thing is called.

        When the thing is a string, a :class:`~godafoss.text`
        is constructed from it and that is written.
        """

        if isinstance( thing, str ):
            thing = gf.text( thing )

        if ink is None:
            thing.write( self, location )
        else:
            thing.write( self, location, ink )

    # =======================================================================

    def clear(
        self,
        ink: [ bool | gf.color ] = False
    ) -> None:
        """
        clear the display

        :param ink: bool
            the 'color' to write to all pixels

        This method clears the display.
        The default implementation writes False to all individual pixels.
        A concrete canvas might implement a faster method.

        A display might be buffered: a clear() call might
        be effectuated only when the flush() method is called.

        $macro_start canvas_clear
        clear the display

        :param ink: (bool)
            the 'color' to write to all pixels

        This method clears the display.
        By default the background 'color' is written to all pixels.
        When ink is true, the inverse of the background is written.

        Writes are buffered: a flush call is required
        to write changed pixels to the screen.
        $macro_end
        """

        ink = self._cure_ink( ink )
        self._dirty = True
        self._clear_implementation( ink )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color | bool ]
    ) -> None:
        """
        write a pixel (concrete implementation)

        :param location: :class:`~godafoss.xy
            the location of the pixel that is to be written

        :param ink: :class:`~godafoss.color`, bool
            the value to be written to the pixel

        This method must be implemented by a concrete class that
        inherits from canvas. When this method is called:
        - the location is within the canvas.
        - for a monochrome canvas, the ink is True.
        - for a color canvas, the ink is a color.
        """

        raise NotImplementedError

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        """
        flush the canvas content (concrete implementation)

        This method must be implemented by a concrete class
        that implements canvas.
        """

        raise NotImplementedError

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ bool | gf.color ]
    ) -> None:
        """
        clear the display (concrete implementation)

        :param ink: bool
            the 'color' to write to all pixels

        This method can be implemented by a concrete class that
        inherits from canvas.
        The default implementation writes False to all individual pixels.
        A concrete canvas might implement a faster method.

        When this method is called:
        - for a monochrome canvas, the ink is a bool.
        - for a color canvas, the ink is a color.
        """

        for x in range( 0, self.size.x ):
            for y in range( 0, self.size.y ):
                self._write_pixel_implementation( gf.xy( x, y ), ink )

    # =======================================================================

    def demo( self ):
        canvas_demo( self )

    # =======================================================================

    def xy_swapped( self ):
        return gf._canvas_transformed(
            self,
            xy( self.size.y, self.size.x ),
            lambda c: xy( c.y, c.x )
        )

    # =======================================================================

    def __add__( self, other ):
        return _add( self, other )

    # =======================================================================

    def combine( self, *args ):
        return _combine( self, *args )

    # =======================================================================

    def extend(
        self,
        other: "canvas",
        direction: str = "EN"
    ) ->"canvas":
        """
        extension of the canvas

        This method returns a canvas that extends the original canvas.

        The direction determines where the other canvas is placed
        relative to the original canvas (north, east, south or west),
        and which side of the canvases is aligned
        (again: north, east, south or west).
        Valid values for the direction are
        "ES", "EN", "WS", "WN", "NW", "NE", "SW", "SE".
        """

        return _extend( self, other, direction )

    # =======================================================================

    def fold(
        self,
        n: int,
        zigzag: bool
    ) -> "canvas":

        return _fold( self, n, zigzag )

    def part(
        self,
        start: gf.xy,
        size: gf.xy
    ):

        """
        part of the canvas

        This method returns a new canvas that is
        part of the original canvas, as specified by the
        start and size parameters.

        The clear() method of a canvas part can be significantly slower
        than the clear() of the original canvas, because it can't use
        the clear() of the driver (which often has a fast way to clear
        the whole canvas).
        """

        return _part( self, start, size )

    # =======================================================================

    def inverted(
        self
    ) -> "canvas":
        """
        inverse of the display

        This method returns a display that inverts the effect
        of write_pixel() calls.
        """

        return _inverted( self )

    # =======================================================================

    def __minus__(
        self
    ) -> "canvas":

        return _inverted( self )

    # =======================================================================

    def rotated(
        self,
        rotation: int
    ) -> "canvas":

        """
        rotated version of the canvas

        This method returns a canvas that is
        a rotated version of the original canvas.
        Allowed rotation values are 0, 90, 180 and 270.
        """

        if rotation == 0:
            return _transformed(
                self,
                self.size,
                lambda c: xy(
                    c.x,
                    c.y
                )
            )

        elif rotation == 90:
            return _transformed(
                self,
                gf.xy( self.size.y, self.size.x ),
                lambda c: gf.xy(
                    self.size.x - 1 - c.y,
                    c.x
                )
            )

        elif rotation == 180:
            return _transformed(
                self,
                self.size,
                lambda c: gf.xy(
                    self.size.x - 1 - c.x,
                    self.size.y - 1 - c.y
                )
            )

        elif rotation == 270:
            return _transformed(
                self,
                gf.xy( self.size.y, self.size.x ),
                lambda c: gf.xy(
                    c.y,
                    self.size.y - 1 - c.x
                )
            )

        else:
            raise ValueError( "rotation must be 0, 90, 180 or 270" )

    # =======================================================================


# ===========================================================================
#
# dummy
#
# ===========================================================================

class canvas_dummy( canvas ):

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        is_color: bool = True,
        background: [ bool | gf.color ] = gf.colors.white,
        palet = {
            gf.colors.white: '.',
            gf.colors.black: '*',
        }
    ):
        canvas.__init__( self, size, is_color, background )
        self._palet = palet
        self._lines = list(
            [ "*" for x in range( self.size.x ) ]
            for y in range( self.size.y )
        )
        self.flush_count = 0

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location,
        ink
    ):
        self._lines[ location.y ][ location.x ] = \
            self._palet[ ink ]

    # =======================================================================

    def lines( self ) -> [ str ]:
        return [
            "".join( self._lines[ y ] )
            for y in range( self.size.y )
        ]

    # =======================================================================

    def __str__( self ) -> [ str ]:
        return "".join( [
            ( '        "' + "".join( self._lines[ y ] ) + '",\n' )
                for y in range( self.size.y ) ] )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self.flush_count += 1

    # =======================================================================


# ===========================================================================
#
# native
#
# ===========================================================================

class canvas_native( canvas ):

    # =======================================================================

    def __init__(
        self,
        size: gf.xy,
        is_color: bool = True,
        background: [ bool | gf.color ] = gf.colors.white,
        name = "godafoss",
        scale = gf.xy( 1, 1 )
    ):
        import PIL
        from PIL import Image
        import graphics

        canvas.__init__( self, size, is_color, background )
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
#
# decorators
#
# ===========================================================================

class _add( canvas ):

    def __init__(
        self,
        a: canvas,
        b: canvas
    ):
        self._a = a
        self._b = b
        canvas.__init__(
            self,
            gf.xy(
                max( self._a.size.x, self._b.size.x ),
                max( self._a.size.y, self._b.size.y )
            ),
            a.is_color and b.is_color,
            a.background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ] = True
    ) -> None:
        self._a.write_pixel( location, ink )
        self._b.write_pixel( location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._a.flush( forced )
        self._b.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ gf.color | bool ] = False
    ) -> None:
        self._a.clear( ink )
        self._b.clear( ink )

    # =======================================================================


# ===========================================================================

class _combine( canvas ):

    def __init__(
        self,
        *args
    ):
        self._list = args
        canvas.__init__(
            self,
            gf.xy(
                max( a.size.x for a in self._list ),
                max( a.size.y for a in self._list )
            ),
            all( a.is_color for a in self._list ),
            self._list[ 0 ]._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ] = True
    ) -> None:
        for x in self._list:
            x.write_pixel( location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        for x in self._list:
            x.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ gf.color | bool ] = False
    ) -> None:
        for x in self._list:
            x.clear( ink )

    # =======================================================================

# ===========================================================================

class _extend( canvas ):

    def __init__(
        self,
        one: canvas,
        other: canvas,
        direction: str
    ) -> None:

        if len( direction ) != 2:
            raise ValueError( "direction must be 2 characters" )
        direction, alignment = direction

        # which canvas comes first
        if direction in "SE":
            a, b = one, other
        elif direction in "NW":
            a, b = other, one
        else:
           raise ValueError( "direction[ 0 ] is invalid" )

        # size depends on extension direction: x or y
        # shift depends on both extension direction and alignment
        if direction in "EW":
            size = gf.xy(
                a.size.x + b.size.x,
                max( a.size.y, b.size.y ) )

            if alignment == "S":
                a_shift = gf.xy( 0,        size.y - a.size.y )
                b_shift = gf.xy( a.size.x, size.y - b.size.y )

            elif alignment == "N":
                a_shift = gf.xy( 0,        0 )
                b_shift = gf.xy( a.size.x, 0 )

            else:
                raise ValueError( "direction[ 1 ] is invalid" )

        elif direction in "NS":
            size = xy(
                max( a.size.x, b.size.x ),
                a.size.y + b.size.y )

            if alignment == "E":
                a_shift = gf.xy( b.size.x - a.size.x, 0 )
                #b_shift = xy( a.size.x, 0 )

            elif alignment == "W":
                a_shift = gf.xy( 0, 0 )
                b_shift = gf.xy( 0, a.size.y )

            else:
                raise ValueError( "direction[ 1 ] is invalid" )

        canvas.__init__( self, size, a.is_color, a._background )
        self._subs = ( ( a, - a_shift ), ( b, - b_shift ) )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ gf.color, bool, None ]
    ) -> None:
        for canvas, offset in self._subs:
            canvas.write_pixel( location + offset, ink )

    # =======================================================================

    def _flush(
        self,
        forced: bool
    ) -> None:
        for canvas, offset in self._subs:
            canvas.flush( forced )

    # =======================================================================

# ===========================================================================

class _fold( canvas ):

    def __init__(
        self,
        subject: canvas,
        n: int,
        zigzag: bool
    ) -> None:
        self._subject = subject
        self._n = n
        self._zigzag = zigzag
        canvas.__init__(
            self,
            gf.xy( subject.size.x // n, subject.size.y * n ),
            is_color = subject.is_color,
            background = subject.background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, gf.color ]
    ) -> None:
        x, y = location.x, location.y
        if self._zigzag and ( ( y % 2 ) == 1 ):
            x = self.size.x - ( x + 1 )
        x = x + self.size.x * ( y // self._subject.size.y )
        y = y % self._subject.size.y
        self._subject.write_pixel( gf.xy( x, y ), ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================

    def _clear_implementation(
        self,
        ink: [ bool, gf. color ]
    ) -> None:
        self._subject.clear( ink )

    # =======================================================================


# ===========================================================================

class _part( canvas ):

    def __init__(
        self,
        subject: canvas,
        start: gf.xy,
        size: gf.xy
    ):
        self._subject = subject
        self._start = start
        canvas.__init__(
            self,
            size,
            subject.is_color,
            subject._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, None ] = True
    ) -> None:
        self._subject.write_pixel( self._start + location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================
    #
    # can't use the subject clear() method, because that
    # would clear all of the subject.
    #
    # =======================================================================

# ===========================================================================

def _invert_ink( ink: [ bool, gf.color ] ):
    return not ink if isinstance( ink, bool ) else - ink

# ===========================================================================

class _inverted( canvas ):

    def __init__(
        self,
        subject: canvas
    ):
        self._subject = subject
        canvas.__init__(
            self,
            subject.size,
            subject.is_color,
            subject._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, gf.color ]
    ) -> None:
        self._subject.write_pixel(
            location,
            _invert_ink( ink )
        )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================


# ===========================================================================

class _transformed( canvas ):
    """
    helper class that is a transformed version of the canvas
    """

    def __init__( self, subject, size, transform_location ):
        self._subject = subject
        self._transform_location = transform_location
        canvas.__init__(
            self,
            size = size,
            is_color = subject.is_color,
            background = subject._background
        )

    def write_pixel(
        self,
        location: gf.xy,
        ink: [ bool, None ] = True
    ) -> None:
        p = self._transform_location( location )
        if self._subject.within( p ):
            self._subject.write_pixel( p, ink )

    # =======================================================================

    def flush(
        self,
        forced: bool = False
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================

    def clear( self, ink: bool = False ) -> None:
        self._subject.clear( ink )

    # =======================================================================


# ===========================================================================
#
# demos
#
# ===========================================================================

def canvas__demo(
    s: gf.canvas,
    iterations = None
):
    print( "canvas demos", s.size )
    pixels = s.size.x * s.size.y

    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            gf.report_memory_and_time()

        if s.is_color:
            canvas_demo_colors( s, iterations = 1 )
            if pixels > 256:
                canvas_demo_color_gradients( s, iterations = 1 )

        if pixels <= 256:
            canvas_demo_blink( s, iterations = 3 )
            canvas_demo_filling( s, iterations = 1 )

        else:
            canvas_demo_lines( s, iterations = 1 )
            canvas_demo_rectangles( s, iterations = 1 )
            canvas_demo_circles( s, iterations = 1 )
            canvas_demo_text( s, iterations = 1 )

        if 0: canvas_demo_scrolling_text(
            s,
            "Hello fantastic brave new world!\nusing Godafoss",
            iterations = 1
        )

        if iteration == 0:
            gf.report_memory_and_time()


# ===========================================================================

def canvas_demo_colors(
    s: gf.canvas,
    pause: int = 1_000_000,
    iterations = None,
):
    print( "canvas demo colors" )

    for _ in gf.repeater( iterations ):

        for c, name in (
            ( gf.colors.red, "RED" ),
            ( gf.colors.green, "GREEN" ),
            ( gf.colors.blue, "BLUE" ),
            ( gf.colors.white, "WHITE" ),
            ( gf.colors.black, "BLACK" ),
        ):
            s.clear( c )
            s.write( name, ink = -c )
            s.flush()
            gf.sleep_us( pause )


# ===========================================================================

def canvas_demo_color_gradients(
    display: gf.canvas,
    pause: int = 50_000,
    iterations = None,
):
    print( "canvas demo colors gradients" )

    for _ in gf.repeater( iterations ):

        steps = 8
        dx = min( 20, ( display.size.x - 2 ) // steps )
        dy = min( 20, ( display.size.y - 2 ) // steps )

        display.clear()
        display.flush()
        gf.sleep_us( pause )

        display.write( gf.rectangle( gf.xy( 2 + steps * dx, 2 + 3 * dy ) ) )
        display.flush()
        gf.sleep_us( pause )

        y = 1
        for c in (
            gf.colors.red,
            gf.colors.green,
            gf.colors.blue
        ):
            ink = c
            x = 1
            for i in range( steps ):
                display.write(
                    gf.rectangle( gf.xy( dx, dy ), fill = True ),
                    location = gf.xy( x, y ),
                    ink = ink
                )
                display.flush()
                gf.sleep_us( pause )
                ink = ( ink // 2 ) + ( ink // 4 )
                x += dx
            y += dy


# ===========================================================================

def canvas_demo_blink(
    s: gf.canvas,
    pause: int =  200_000,
    iterations = None,
    sequence = ( True, False )
):
    print( "canvas demo blink" )

    for _ in gf.repeater( iterations ):

        for c in sequence:
            s.clear( c )
            s.flush()
            gf.sleep_us( pause )


# ===========================================================================

def canvas_demo_filling(
    s: gf.canvas,
    pause: int =  100_000,
    iterations = None,
    sequence = ( True, False )
):
    print( "canvas demo filling" )

    for _ in gf.repeater( iterations ):
        s.clear()
        s.flush()
        for color in sequence:
            for p in range( 0, s.size.x + s.size.y ):
                s.write(
                    gf.line( gf.xy( - ( p + 1 ), p + 1 ) ),
                    gf.xy( p, 0 ),
                    color
                )
                s.flush()
                gf.sleep_us( pause )


# ===========================================================================

def canvas_demo_lines(
    s : gf.canvas,
    iterations: None = None,
    frame = True
):

    print( "canvas demo lines" )

    for _ in gf.repeater( iterations ):

        s.clear()
        if frame:
            s.write( gf.rectangle( s.size ) )
            s.flush()

        for _ in range( 0, 20 ):
            start = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            end = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            s.write( gf.line( end - start ) @ start )
            s.flush()
            gf.sleep_us( 100_000 )

        gf.sleep_us( 2_000_000 )

# ===========================================================================

def canvas_demo_rectangles(
    s : gf.canvas,
    iterations = None,
    frame = True
):

    print( "canvas demo rectangles" )

    for _ in gf.repeater( iterations ):

        s.clear()
        if frame:
            s.write( gf.rectangle( s.size ) )
            s.flush()

        for dummy in range( 0, 10 ):
            start = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            end = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( gf.rectangle( end - start ) @ start )
            s.flush()
            gf.sleep_us( 100_000 )

        gf.sleep_us( 2_000_000 )


# ===========================================================================

def canvas_demo_circles(
    s : gf.canvas,
    iterations = None,
    frame = True
):

    print( "canvas demo circles" )

    for _ in gf.repeater( iterations ):

        s.clear()
        if frame:
            s.write( gf.rectangle( s.size ) )
            s.flush()

        for _ in range( 0, 20 ):
            start = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            radius = randint( 0, min( s.size.x, s.size.y ) // 2 )
            end = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( gf.circle( radius ) @ start )
            s.flush()
            gf.sleep_us( 100_000 )

        gf.sleep_us( 2_000_000 )


# ===========================================================================

def canvas_demo_text(
    s : gf.canvas,
    iterations = None,
    frame = True
):

    print( "canvas demo text" )

    for _ in gf.repeater( iterations ):

        s.clear()
        if frame:
            s.write( gf.rectangle( s.size ) )
            s.flush()
            gf.sleep_us( 500_000 )

        s.write( gf.text( "Hello world" ) @ gf.xy( 1, 1 ) )
        s.flush()
        gf.sleep_us( 500_000 )

        s.write( gf.text( "Micropython" ) @ gf.xy( 1, 9 ) )
        s.flush()
        gf.sleep_us( 500_000 )

        s.write( gf.text(  "+ Godafoss" ) @ gf.xy( 1, 17 ) )
        s.flush()
        gf.sleep_us( 2_000_000 )

# ===========================================================================

def canvas_demo_ggf_photos(
    s: gf.canvas,
    location: str,
    iterations = None
):
    import os

    print( "canvas demo ggf photos\non %s lcd" % s.size )

    s.clear()
    s.write( text( "SD card photos demo\nfrom %s" % location ) )
    s.flush()

    files = list( os.listdir( location ) )
    files.sort()

    for _ in gf.repeater( iterations ):

        for name in files:
            print( "next file %s" % name )
            s.clear()
            elapsed = gf.elapsed_us( lambda :
                s.write(
                    ggf( location + "/" + name ),
                    xy( 0, 24 )
                )
            )
            s.write(
                text( "file %s/%s\nloaded in %d ms" %
                    ( location, name, elapsed // 1000 )
                )
            )
            s.flush()

# ===========================================================================

def canvas_demo_scrolling_text(
    s: gf.canvas,
    t: [ str, gf.text ],
    scroll_pause: int =  100,
    end_pause: int = 1_000_000,
    iterations = None,
):
    print( "canvas demo scrolling text" )

    if isinstance( t, str ):
        t = text( t )

    for _ in repeater( iterations ):
        for x in range( 0, t.size.x - s.size.x ):
            s.clear()
            s.write( t @ gf.xy( - x, 0 ) )
            s.flush()
            gf.sleep_us( scroll_pause )
        gf.sleep_us( end_pause )


# ===========================================================================
