# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_t_dongle_s3.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

#$$document( 0 )


# ===========================================================================

class board_lilygo_ttgo_t_dongle_s3:

    """
    $$insert_image( "lilygo_ttgo_t_dongle_s3_python", 300 )
    $$insert_image( "lilygo_ttgo_t_dongle_s3_back", 380 )
    $$add_table( "boards", "board_lilygo_ttgo_t_dongle_s3", "lilygo_ttgo_t_dongle_s3_python" )    
    
    `manufacturers documentation on github 
    <https://github.com/Xinyuan-LilyGO/T-Dongle-S3>`_
    
    +------------------------+----------------------------------------------+
    | uC                     | esp32s3 (dual core)                          |
    +------------------------+----------------------------------------------+
    | Flash                  | W25Q32 8 Mb                                  |
    +------------------------+----------------------------------------------+
    | WiFi                   | ESP32, onboard chip antenna                  |
    +------------------------+----------------------------------------------+
    | OLED                   | ST7735 0.96" 80 x 160 color                  |
    +------------------------+----------------------------------------------+
    | USB                    | A (no auto-load circuit)                     |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 6 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 249088                                       |
    +------------------------+----------------------------------------------+

    This is an esp32s3 (dual core LX7) dongle with an ST7735 0.96" 
    80 x 160 SPI color LCD, a single (bootload) button, 
    an APA102 neopixel and an SD card slot
    (which is hidden inside the USB A connector).
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | button (low when pressed)                                      |
    +-----+----------------------------------------------------------------+
    |  39 | led_ci                                                         |
    +-----+----------------------------------------------------------------+
    |  40 | led_di                                                         |
    +-----+----------------------------------------------------------------+
    |   5 | spi_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |   3 | spi_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |  16 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |   4 | tft_rst                                                        |
    +-----+----------------------------------------------------------------+
    |   4 | tft_bl (active low)                                            |
    +-----+----------------------------------------------------------------+
    """

    # =======================================================================

    def __init__( self ):
        self.button = 0

        self.led_ci = 39
        self.led_di = 40

        self.spi_sclk = 5
        self.spi_mosi = 3
        
        self.tft_cs = 4
        self.tft_dc = 2
        self.tft_rst = 1
        self.tft_bl = 38
          
    # =======================================================================
       
    def spi( 
        self, 
        baudrate = 1_000_000,
        polarity = 1,
        phase = 1       
    ):
        """
        the (soft) SPI bus
        """
        
        import machine
        return machine.SoftSPI(
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sclk ),
            mosi = machine.Pin( self.spi_mosi ),

            # dummy
            miso = machine.Pin( 6 )
        )
        
    # =======================================================================

    def display(
        self,
        rotate = False,
        monochrome = False
    ):
        """
        the LCD
        
        :param rotate: bool       
        True when the dongle is to be used with
        its USB connector at the right
        
        :param monochrome: bool        
        True to use the display in monochrome mode
        """
        
        return gf.st7735(
            size = gf.xy( 160, 80 ),
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            swap_xy = True,
            invert = True,
            mirror_y = rotate,
            mirror_x = not rotate,
            offset = gf.xy( 1, 26 ),
            reset = self.tft_rst,
            backlight = gf.make_pin_out( self.tft_bl ).inverted(),
            color_order = None if monochrome else "BGR",
        )
                
    # =======================================================================
        
    def neopixel( self ):
        """
        the single neopixel
        """        
        
        return gf.apa102(
            n = 1, 
            ci = self.led_ci,
            di = self.led_di,
        )
        
    # =======================================================================
        
# ===========================================================================
