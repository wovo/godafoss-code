# ===========================================================================
#
# file     : lilygo_ttgo_t_qt_pro_display.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_t_qt_pro()
display = board.display()
python = gf.ggf( "micropython_128_128.ggf" )

display.clear()
display.write( python )
display.flush()