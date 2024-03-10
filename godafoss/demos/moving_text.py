# ===========================================================================
#
# file     : moving_text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def moving_text(
    s: gf.canvas,
    t: [str, gf.text ],
    pixel_pause: int =  1_000,
    text_pause: int = 1_000_000,
    iterations = None,
) -> None:
    for _ in gf.repeater( iterations ):
        for x in range( 0, t.size.x - s.size.x ):
            s.clear()
            s.write( t @ xy( - x, 0 ) )
            s.flush()
            gf.sleep_us( pixel_pause )
        gf.sleep_us( text_pause )


