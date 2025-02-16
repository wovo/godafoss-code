import godafoss as gf
from machine import SPI
from machine import Pin
import time

class gopherbadge:
    led = gf.pin_out( 2 )
    backlight = gf.pin_out( 12 )
    neopixels = gf.ws281x( 15, 2 )
    lcd_spi = SPI(0, baudrate=12000000, phase=0, polarity=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    audio = gf.pin_out( 14 )
    audio_enable = gf.pin_out( 3 )
    display = gf.generic_color_lcd(
        spi = lcd_spi,
        data_command = 20,
        chip_select = 17,
        reset = 21,
        backlight = 12,
        #power = None,
        
        mechanism = 0,
        background = gf.colors.black,
        monochrome = False,
        invert = True,
        orientation = gf.orientation.south,
        
        # display-specific parameters
        size = gf.xy( 120, 60 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = gf.xy( 0, 0 ),
        x_deadband = 0
        
    )

#gopherbadge.led.demo()
#gopherbadge.backlight.blink()
# gopherbadge.neopixels.demo_color_wheel()
#gopherbadge.display.demo()
gopherbadge.audio_enable.write( 1 )
for i in range( 500 ):
    gopherbadge.audio.write( 1 )
    time.sleep( 0.001 )
    gopherbadge.audio.write( 0 )
    time.sleep( 0.001 )
    
