# ===========================================================================
#
# file     : luatos_core_esp32c3_air101_python.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# source time 19612 ms, memory 68944 bytes (199984->131040)

import godafoss as gf
board = gf.board_luatos_core_esp32c3()
display = board.air101_display()
python = gf.ggf( "python_80_82.ggf" )

display.clear()
display.write( python )
display.flush()
gf.report_memory_and_time()