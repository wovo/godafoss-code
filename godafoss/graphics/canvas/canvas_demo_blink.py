# ===========================================================================
#
# file     : canvas_demo_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


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
