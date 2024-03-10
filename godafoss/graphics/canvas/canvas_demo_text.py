# ===========================================================================
#
# file     : canvas_demo_text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

from random import randint

import godafoss as gf


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
