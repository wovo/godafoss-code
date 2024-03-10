# ===========================================================================
#
# file     : gf_edge.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================
#
# This file provides the 'abstract' interfaces that my 'edge' lab 
# target boards provide: for each target, a 14-pin header provides
# ground, power, and 8 data pins (p0..p7).
# Some of these pins also function as soft and hards SPI and I2C 
# interfaces.
#
# Some pins have dedicated functions when interfacing to 
# typical peripherals using soft and hard SPI and I2C, and
# for peripheral pins like chipo_select, data_command, reset
# background, etc.
#
# ===========================================================================

import os
import godafoss as gf
silent = False


# ===========================================================================

def edge():
    try:
        uname = os.uname()
    except:
        result = gf._edge_native()
        
    if uname[ 0 ] == "rp2":
        result = gf._edge_rp2()
            
    elif uname[ 0 ] == "esp32":
        
        if uname[ 4 ] == "ESP32C3 module with ESP32C3":
            result = gf._edge_esp32c3()
            
        elif uname[ 4 ] == "LOLIN_S2_PICO with ESP32-S2FN4R2":
            result = gf._edge_esp32_lolin_c2_pico()
                
        elif uname[ 4 ] == "LOLIN_C3_MINI with ESP32-C3FH4":
            result = gf._edge_esp32_lolin_c3_mini()
                
        else:
            result = gf._edge_esp32()
                
    elif uname[ 0 ] == "esp8266":      
        result = gf._edge_esp8266()                 
    
    elif uname[ 0 ] == "mimxrt":
        result = gf._edge_mimxrt()
            
    else:
        print( "unknow uname:", uname[ 0 ] )
            
    if not silent:
        print( "edge board is", result.system )
        print( "edge pins are", result.pins )       
        
    result.p0, result.p1, result.p2, result.p3, result.p4, \
        result.p5, result.p6, result.p7 = result.pins
        
    # (soft) SPI        
    result.spi_sck = result.p0
    result.spi_mosi = result.p1
    result.spi_miso = result.p2

    # lcd
    result.chip_select = result.p3
    result.data_command = result.p4
    result.reset = result.p5
    result.backlight = result.p6

    # (soft) I2C
    result.i2c_scl = result.p6
    result.i2c_sda = result.p7

    # neopixels
    result.neopixel_data = result.p5        

    return result        
        
