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
board = gf.board_01space_rp2040_042lcd()
neopixel = board.neopixel()

neopixel.demo()
