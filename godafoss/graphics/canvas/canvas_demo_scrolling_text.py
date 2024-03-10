# ===========================================================================
#
# file     : canvas_demo_scrolling_text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

from random import randint

import godafoss as gf


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
