# ===========================================================================
#
# file     : canvas__demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
from random import randint


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
