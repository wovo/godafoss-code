# ===========================================================================
#
# file     : sunton_esp32_173s019_display.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the godafoss __init__.py
#
# ===========================================================================

# 2024-04-05
# python sources
# plain  time 36285 ms, memory 138176 bytes (248640->110464)
# spiram time 33756 ms, memory 159904 bytes (8317760->8157856)
# mpy sources
# plain  time  2484 ms, memory 134272 bytes (249344->115072)
# spiram time  2216 ms, memory 154832 bytes (8318448->8163616)
# frozen
# plain  time   519 ms, memory 121776 bytes (251312->129536)
# spiram time   394 ms, memory 142304 bytes (8320432->8178128)


import godafoss as gf
board = gf.board_sunton_esp32_173s019()
display = board.display( rotate = True, horizontal = True )

display.demo()