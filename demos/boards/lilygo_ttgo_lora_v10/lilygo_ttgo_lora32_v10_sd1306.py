# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_lora32_v10_sd1306.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_lora32_v10()
display = board.display()

display.demo()

