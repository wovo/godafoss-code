# ===========================================================================
#
# file     : canvas_demo_filling.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


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
