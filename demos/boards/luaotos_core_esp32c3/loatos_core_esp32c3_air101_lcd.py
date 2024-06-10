# ===========================================================================
#
# file     : luatos_core_esp32c3_air101_lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
board = gf.board_luatos_core_esp32c3()
display = board.air101_display()

display.demo()


