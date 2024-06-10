# ===========================================================================
#
# file     : canvas_demo_colors.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from random import randint

import godafoss as gf
#

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
