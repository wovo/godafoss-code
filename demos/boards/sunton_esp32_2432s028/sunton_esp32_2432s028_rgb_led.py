# ===========================================================================
#
# file     : sunton_esp32_2432s028_rgb_leds.py
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

red = gf.make_pin_out( board.red_led_pin ).inverted()
green = gf.make_pin_out( board.green_led_pin ).inverted()
blue = gf.make_pin_out( board.blue_led_pin ).inverted()

red.write( 0 )
green.write( 0 )
blue.write( 0 )

iterations = 3

while True:
    red.demo( iterations = iterations )
    green.demo( iterations = iterations )
    blue.demo( iterations = iterations )
