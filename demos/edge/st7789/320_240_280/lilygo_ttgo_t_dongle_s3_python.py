# ===========================================================================
#
# file     : lilygo_t_dongle_s3_python.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.glcd(      
    size = gf.xy( 320, 240 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    mirror_x = True,
    swap_xy = True
)

python = gf.ggf( "python_233_240.ggf" )

display.clear()
display.write( python )
display.flush()