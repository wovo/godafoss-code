# ===========================================================================
#
# file     : sunton_esp32_2432s028_display.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the godafoss __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_sunton_esp32_2432s028()
display = board.display( color_order = None )
display.demo()