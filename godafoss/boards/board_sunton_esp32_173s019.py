# ===========================================================================
#
# file     : gf_board_sunton_esp32_173s019.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from micropython import const

import godafoss as gf


# ===========================================================================

class board_sunton_esp32_173s019:

    """
    $$insert_image( "sunton_esp32_173s019_python", 300 )
    $$insert_image( "sunton_esp32_173s019_back", 300 )
    $$add_table( "boards", "board_sunton_esp32_173s019", "sunton_esp32_173s019_python" )
    
    `manufacturers documentation (zip)
    <http://pan.jczn1688.com/directlink/1/ESP32%20module/1.9inch_ESP32-1732S019.zip>`_
    
    +------------------------+----------------------------------------------+
    | uC                     | esp32s3 (dual core)                          |
    +------------------------+----------------------------------------------+
    | Flash                  | 16 Mb                                        |
    +------------------------+----------------------------------------------+
    | SPIRAM (octal)         | 8 Mb                                         |
    +------------------------+----------------------------------------------+
    | LCD                    | ST7789 1.9" 320 x 170 color                  |
    +------------------------+----------------------------------------------+
    | USB                    | C, CH340, boot & reset circuit,              |
    |                        | linear regulator                             |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 6 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 249216 (without SPIRAM)                      |
    |                        | 8193360 (with SPIRAM)                        |
    +------------------------+----------------------------------------------+    

    This is an ESP32-S3 board with 8Mb octal SPIARM, 
    an ST7789 1.9" 320 x 170 color LCD,
    and boot and reset buttons.
    The CH340 usb-serial interface supports hands-off bootloading.
    It also has a small connector that is mentioned in the documentation
    as a TF card connector, but I don't think it is. 
    
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | boot_mode_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  12 | lcd_sclk_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  13 | lcd_mosi_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  11 | lcd_rs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  10 | lcd_cs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |   1 | lcd_reset_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  14 | lcd_backlight_pin                                              |
    +-----+----------------------------------------------------------------+
    """
    
    # =======================================================================
           
    boot_mode_pin      = const(  0 )
        
    lcd_sclk_pin       = const( 12 )
    lcd_mosi_pin       = const( 13 )
    lcd_rs_pin         = const( 11 )
    lcd_cs_pin         = const( 10 )
    lcd_reset_pin      = const(  1 )
    lcd_backlight_pin  = const( 14 )      

    # =======================================================================
           
    def __init__( self ):
        pass
    
    # =======================================================================
           
    def display(
        self,
        rotate = False,
        monochrome = False,
        horizontal = False,
    ):
        
        import machine
        spi = gf.spi(
            id = 1,
            frequency = 30_000_000,
            sck = self.lcd_sclk_pin,
            mosi = self.lcd_mosi_pin,
            miso = 15 # dummy
        )        
        return gf.st7789(
            size = gf.xy( 320, 170 ) if horizontal else gf.xy( 170, 320 ), 
            spi = spi,
            data_command = self.lcd_rs_pin,
            chip_select = self.lcd_cs_pin,
            reset = self.lcd_reset_pin,
            backlight = self.lcd_backlight_pin,
            invert = True,
            mirror_y = rotate,
            mirror_x = rotate != horizontal,
            swap_xy = horizontal,
            color_order = None if monochrome else "RGB",
            offset = gf.xy( 0, 35 ) if horizontal else gf.xy( 35, 0 )
        )
        
# ===========================================================================