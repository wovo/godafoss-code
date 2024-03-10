# ===========================================================================
#
# file     : 01space_rp2040_042lcd_display.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import godafoss as gf

display = gf.hub75(
    size = gf.xy( 128, 32 ),
    r1_b2 = 2,
    a_e = 10,
    clk_lat_oe = 26,
    frequency = 2_000_000
)#.folded( 2 )

if 0:
 d = display
 d.clear()
 d.write( gf.rectangle( gf.xy( -10, -10 ) ), gf.xy( 20, 20 ) )
 d.write( gf.rectangle( gf.xy( 10, 10 ) ), gf.xy( 30, 30 ) )
 d.flush()

if 1:
 display.demo()

if 0:
 for c in [ gf.colors.red, gf.colors.green, gf.colors.blue ]:
    print( c )
    display.clear( c ) 
    if 0:
     display.write(
        gf.rectangle( display.size - gf.xy( 10, 10 ), fill = True ),
        gf.xy( 5, 5 ),
        gf.colors.black
    )
    display.flush()
    gf.sleep_us( 1_000_000 )
