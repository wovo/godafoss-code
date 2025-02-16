# ===========================================================================
#
# file     : uc8151.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : modified by Wouter van Ooijen <wouter@voti.nl> 2025
#          : original by Salvatore Sanfilippo <antirez@gmail.com> 2024
# license  : MIT license, see license attribute (godafoss.license)
#
# ===========================================================================

import godafoss as gf

import machine
from machine import Pin
import framebuf
import time

class badger2040:
    def __init__(
        self
    ) -> None:
        spi = SPI(0, baudrate=12000000, phase=0, polarity=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.display = gf.UC8151(
            spi,
            cs = 17,
            dc = 20,
            rst = 21,
            busy = 26,
            speed = 2,
            no_flickering = False
        )


# ===========================================================================

if  __name__ == "__main__":
    from machine import SPI
    from random import randint

    eink = badger2040()
    eink.display.clear()
    
    s = eink.display
    for _ in gf.repeater( 0 ):

        if 1:
            s.write( gf.rectangle( s.size ) )
            s.flush()
            
        s.write( gf.text( "Hello world" ), gf.xy( 10, 10 ) )            

        if 0:
         for dummy in range( 0, 10 ):
            start = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            end = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( gf.rectangle( end - start ) @ start )
    
    s.write( gf.rectangle( gf.xy( 100, 11 ) ) @ gf.xy( 0, 0 ) )
    s.write( gf.text( "Hello world" ), gf.xy( 1, 2 ) )            
    eink.display.flush()

