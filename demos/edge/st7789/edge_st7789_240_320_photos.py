# ===========================================================================
#
# file     : edge_st7789_240_320_sd_card_photos.py
# part of  : godafoss micropython library edge demos
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : this file is in  the public domain
#
# This demo shows pictures .ggf from the /sdcard directory
# on an st7789 240 x 320 (portrait mode) LCD.
#
# ===========================================================================

import godafoss as gf
import edge

photos_location = "/sdcard"

spi = edge.hard_spi( 1, 20_000_000 )
# spi = edge.soft_spi()

# ===========================================================================

display = gf.st7789(
    size = gf.xy( 240, 320 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    order = "BRG",
)

display.demo_ggf_photos( photos_location ) 

# ===========================================================================


