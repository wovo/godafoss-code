
# https://github.com/Xinyuan-LilyGO/TTGO-LoRa-Series

import godafoss as gf
import machine

reset = gf.gpio_out( 16 )
reset.write( 1 )

i2c = machine.SoftI2C(
        scl = machine.Pin( 15, machine.Pin.OUT ),
        sda = machine.Pin(  4, machine.Pin.OUT )
    )

gf.ssd1306_i2c(
    gf.xy( 128, 64 ),
    i2c
).demo()