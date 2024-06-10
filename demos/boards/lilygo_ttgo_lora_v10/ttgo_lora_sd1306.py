
# https://github.com/Xinyuan-LilyGO/TTGO-LoRa-Series

import godafoss as gf
board = gf.board_lilygo_ttgo_lora32_v10()
display = board.display()

display.demo()


import machine

reset = gf.gpio_out( 16 )
reset.write( 1 )

i2c = machine.SoftI2C(
        scl = machine.Pin( 15 ),
        sda = machine.Pin(  4 )
    )

gf.ssd1306_i2c(
    gf.xy( 128, 64 ),
    i2c
).demo()