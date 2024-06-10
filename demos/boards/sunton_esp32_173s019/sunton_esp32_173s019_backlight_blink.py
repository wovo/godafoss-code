# ===========================================================================
#
# file     : sunton_esp32_173s019_backlight_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# ===========================================================================

# spiram
# sources time 38588 ms, memory 160416 bytes (8317728->8157312)
# mpy     time  2701 ms, memory 154752 bytes (8318432->8163680)
# frozen  time   426 ms, memory 142656 bytes (8320400->8177744)

import godafoss as gf
board = gf.board_sunton_esp32_173s019()

display = board.display()
display.clear( gf.colors.green )
display.flush()

display._backlight.demo( period = 1_000_000 )