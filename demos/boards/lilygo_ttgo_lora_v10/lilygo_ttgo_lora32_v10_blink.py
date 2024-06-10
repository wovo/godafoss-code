# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_lora32_v10_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_lora32_v10()

gf.blink( board.led )
