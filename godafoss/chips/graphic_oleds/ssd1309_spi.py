# ===========================================================================
#
# file     : gf_ssd1309_spi.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from micropython import const
import machine
import framebuf

import godafoss as gf

# ===========================================================================

class ssd1309_spi(
    gf.lcd_reset_backlight_power, 
    gf.lcd_spi_cd,
    gf.ssd1309_base
):
    """
    ssd1309 spi monochrome oled display driver
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param spi: (machine.SPI)
        spi bus that connects to the chip (miso not used)
    
    :param data_command: ($macro_insert make_pin_out_types )
        dc (data/command) pin of the chip 
        
    :param chip_select: ($macro_insert make_pin_out_types )
        cs (chip select) pin of the chip   

    :param reset: (None, $macro_insert make_pin_out_types )
        reset pin of the chip, active low;
        optional, the pin can be connected to Vcc (3.3V).
    
    :param background: (bool)
        background 'color', default (False) is off
    
    This is a spi driver for the ssd1306 monochrome oled controller.
    This chip is used in various cheap oled displays and modules.
    
    #$insert_image( "ssd1306-spi", 1, 200 )
    
    $macro_insert canvas_monochrome      
    """
    
    # =======================================================================

    def __init__( 
        self, 
        size: xy, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ], 
        chip_select: [ int, pin_out, pin_in_out, pin_oc ], 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        background = False 
    ) -> None:
        gf.lcd_reset_backlight_power.__init__(
            self,
            reset = gf.make_pin_out( reset ).inverted(),
            backlight = None,
            power = None
        ) 
        gf.lcd_spi_cd.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select
        )         
        gf.ssd1309_base.__init__(
            self, size = size,
            background = background
        )

    # =======================================================================
    
    def _write_framebuf( self ) -> None:
        self.write_command( None, buffer = self._buffer )

    # =======================================================================
    
# ===========================================================================
