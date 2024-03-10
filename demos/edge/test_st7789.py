# code for micropython 1.10 on esp8266

import random

import machine
import st7789py as st7789
import time

spi= machine.SoftSPI( 
            baudrate=4000000,
            polarity=1,
            phase=1,
            sck = machine.Pin( 14, machine.Pin.OUT ),
            mosi = machine.Pin( 15, machine.Pin.OUT ),
            miso = machine.Pin( 16, machine.Pin.IN )
        )


def main():
    print( "st7789" )
    display = st7789.ST7789(
        spi, 128, 128,
        reset=machine.Pin(19, machine.Pin.OUT),
        dc=machine.Pin(18, machine.Pin.OUT),
        cs=machine.Pin(17, machine.Pin.OUT),
        xstart = 2,
        ystart = 1
    )
    machine.Pin(17, machine.Pin.OUT)( 1 )
    display.init()

    while True:
        #display.fill( 0xF800 )
        #display.fill( 0x07E0 )
        #display.fill( 0x001F )
        display.fill( 0x0000 )
        display.rect( 2, 2, 124, 124, 0xFFFF )
        break
        
        
main()

"""
            st7789.color565( 
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8),
            ),
"""            
