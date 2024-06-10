# ===========================================================================
#
# file     : canvas_demo_lines.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
from random import randint


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
