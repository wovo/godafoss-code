# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_t_camera_mini.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

# ligt in camera bakje
#$$document( 0 )

import godafoss as gf


# ===========================================================================

class board_lilygo_ttgo_t_camera_mini:

    """
    $insert_image( "lilygo_ttgo_t_camera_mini", 1, 300 )
    
    manufacturers documentation on github:
    
    `this model
    <https://github.com/Xinyuan-LilyGO/TTGO_Camera_Mini>`_
    
    `lilygo camera series
    <https://github.com/Xinyuan-LilyGO/LilyGo-Camera-Series>`_
    
    +------------------------+-------------------------------------------+
    | uC                     | esp32-d0wdq5                              |
    +------------------------+-------------------------------------------+
    | Flash                  | W25Q128 16Mb                              |
    +------------------------+-------------------------------------------+
    | SPIRAM                 | ips6404 8Mb                               |
    +------------------------+-------------------------------------------+
    | camera                 | OV2640                                    |
    +------------------------+-------------------------------------------+
    | LiPo                   | 400 mAH, AXP192                           |
    +------------------------+-------------------------------------------+
    | USB                    | mini, CP2104                              |
    +------------------------+-------------------------------------------+
    | MicroPython free Flash | x Mb                                      |
    +------------------------+-------------------------------------------+
    | MicroPython free RAM   | x                                         |
    +------------------------+-------------------------------------------+
    
    23, 18 @ edge

    This is a small white enclosure with 
    an 400mAH LiPo and an ESP32 board.
    The board has a camera, one capacitive touch input, 
    two buttons (power and reset), a USB interface,
    and an axp192 charging circuit for the LiPo.

    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |

    +-----+----------------------------------------------------------------+
    """

    # =======================================================================

    def __init__( self ):
    
        self.axp192_i2c_scl = 22
        self.axp192_i2c_sda = 21
        self.axp192_irq = 35
        
        self.ov2640_power = 26
        self.ov2640_y = ( 5, 14, 4, 15, 37, 38, 36, 39 )
        self.ov2640_pclk = 29
        self.ov2640_vsync = 27
        self.ov2640_href = 25
        self.ov2640_xclk = 32
        self.ov2640_sio_clk = 12
        self.ov2640_sio_dat = 13
        

          
    # =======================================================================
       
    def spi( 
        self, 
        baudrate = 1_000_000,
        polarity = 1,
        phase = 1       
    ):
        """
        the (hard) SPI bus
        """
        
        import machine
        return machine.SPI(
            1,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sclk ),
            mosi = machine.Pin( self.spi_mosi ),

            # dummy, the default MISO pin is used for the tft_rst
            miso = machine.Pin( 23 )
        )
        
    # =======================================================================

    def display_monochrome( self ):
        """
        the LCD (monochrome driver)
        """        
        return gf.st7789(
            size = gf.xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = gf.xy( 51, 40 ),
            x_deadband = 0,
            color_order = None,
            # lookup_table = False
        )
        
    # =======================================================================

    def display( self ):
        """
        the LCD (color driver)
        """        
        return gf.st7789(
            size = gf.xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = gf.xy( 52, 40 )
        )
        
    # =======================================================================
        
# ===========================================================================
