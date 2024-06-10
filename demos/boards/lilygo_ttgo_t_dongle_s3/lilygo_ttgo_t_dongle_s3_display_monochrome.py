# ===========================================================================
#
# file     : lilygo_t_dongle_s3_display_monochrome.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_t_dongle_s3()
display = board.display_monochrome()

display.demo()