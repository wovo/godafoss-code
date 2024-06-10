# ===========================================================================
#
# file     : canvas_demo_ggf_photos.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from random import randint

import godafoss as gf


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
