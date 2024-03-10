# ===========================================================================
#
# file     : sunton_esp32_2432s028_ldr.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import godafoss as gf
board = gf.board_sunton_esp32_2432s028()
ldr = gf.gpio_adc( board.ldr_pin )

while True:
    print( ldr.read() )
    gf.sleep_us( 500_000 )
