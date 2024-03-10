# ===========================================================================
#
# file     : canvas_demo_circles.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

from random import randint

import godafoss as gf


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
