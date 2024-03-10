# ===========================================================================
#
# file     : sunton_esp32_173s019_display.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the godafoss __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_sunton_esp32_173s019()
display = board.display()

display.demo()