# ===========================================================================
#
# file     : lilygo_ttgo_t_wristband_siaplsy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import godafoss as gf
board = gf.board( "lilygo_ttgo_t_wristband" )

display = board.display()
display.demo()
