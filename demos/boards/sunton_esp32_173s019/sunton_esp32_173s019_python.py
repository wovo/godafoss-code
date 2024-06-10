# ===========================================================================
#
# file     : board_sunton_esp32_173s019.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# requires spiram
# source time 62888 ms, memory 203072 bytes (8317680->8114608)
# mpy    time 23053 ms, memory 200816 bytes (8318368->8117552)
# frozen time 20673 ms, memory 185104 bytes (8320048->8134944)

import godafoss as gf
board = gf.board_sunton_esp32_173s019()
display = board.display( horizontal = True )
python = gf.ggf( "python_165_170.ggf" )

display.clear()
display.write( python )
display.flush()
gf.report_memory_and_time()