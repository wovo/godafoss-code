# ===========================================================================
#
# file     : lilygo_t_watch_2020_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the godafoss __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import godafoss as gf
board = gf.board( "lilygo_ttgo_t_watch_2020" )
backlight = gf.make_pin_out( board.tft_bl )

if 1:
    import machine
    i0 = machine.SoftI2C(sda=machine.Pin(21),scl=machine.Pin(22))    
    power_output_control = i0.readfrom_mem(53, 0x12, 1)[0]
    power_output_control |= 4 # LDO2 enable
    i0.writeto_mem(53, 0x12, bytes([power_output_control]))  

backlight.demo( iterations = 20 )
