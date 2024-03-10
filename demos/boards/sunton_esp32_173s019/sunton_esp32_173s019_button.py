# ===========================================================================
#
# file     : sunton_esp32_173s019_button.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import godafoss as gf
board = gf.board_sunton_esp32_173s019()
button = gf.make_pin_in( board.boot_mode_pin )

button.demo()