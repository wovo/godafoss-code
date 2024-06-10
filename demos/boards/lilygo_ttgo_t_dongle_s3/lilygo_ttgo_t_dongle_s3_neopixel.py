# ===========================================================================
#
# file     : lilygo_t_dongle_s3_neopixel.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_t_dongle_s3()
pixel = board.neopixel()

pixel.demo_color_wheel( delay = 1_000_000 )