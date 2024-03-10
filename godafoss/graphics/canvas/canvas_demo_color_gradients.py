# ===========================================================================
#
# file     : canvas_demo_color_gradients.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

from random import randint

import godafoss as gf


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
