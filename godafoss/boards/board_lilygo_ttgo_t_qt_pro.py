# ===========================================================================
#
# file     : gf_board_lilygo_t_qt_pro.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class board_lilygo_ttgo_t_qt_pro:

    """
    $$insert_image( "lilygo_ttgo_t_qt_pro_python", 300 )
    $$insert_image( "lilygo_ttgo_t_qt_pro_back", 300 )
    $$add_table( "boards", "board_lilygo_ttgo_t_qt_pro", "lilygo_ttgo_t_qt_pro_python" )
    
    `manufacturers documentation on github
    <https://github.com/Xinyuan-LilyGO/T-QT>`_
    
    +------------------------+----------------------------------------------+
    | uC                     | esp32s3 (dual core LX7)                      |
    +------------------------+----------------------------------------------+
    | Flash                  | 8 Mb                                         |
    +------------------------+----------------------------------------------+
    | WiFi                   | ESP32, onboard chip antenna, U.FL connector  |
    +------------------------+----------------------------------------------+
    | LCD                    | GC9107 0.85" 128 x 128 color                 |
    +------------------------+----------------------------------------------+
    | USB                    | C (no auto-load circuit)                     |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 6 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 249536                                       |
    +------------------------+----------------------------------------------+

    This is a very small ESP32 board with a 128 x 128 SPI color LCD, 
    two input buttons left and right of the USB connector, 
    and a reset button at the side of the board.
    A small molex connector provides gnd, 3.3V and two gpio pins.
    There is an on-board chip antenna, and an antenna connector
    (requires re-soldering a 0 ohm resistor).
    
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  47 | button2_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   3 | spi_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |   2 | spi_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |   6 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |   1 | tft_rst                                                        |
    +-----+----------------------------------------------------------------+
    |  10 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    """

    # =======================================================================

    def __init__( self ):
    
        self.button1_pin = 0
        self.button2_pin = 47
        
        self.spi_sclk = 3
        self.spi_mosi = 2
        
        self.tft_cs = 5
        self.tft_dc = 6
        self.tft_rst = 1
        self.tft_bl = 10
          
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
            miso = machine.Pin( 4 )
        )
               
    # =======================================================================

    def display(
        self,
        rotate = False,
        monochrome = False
    ):
        """
        the LCD (color driver)
        """        
        gf.make_pin_out( self.tft_rst ).write( 1 )
        return gf.st7735(
            size = gf.xy( 128, 128 ),
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            swap_xy = True,
            invert = True,
            mirror_y = rotate,
            mirror_x = not rotate,
            offset = gf.xy( 1, 2 ),
            reset = self.tft_rst,
            backlight = gf.make_pin_out( self.tft_bl ).inverted(),
            color_order = None if monochrome else "BGR",
        )
        
    # =======================================================================
        
# ===========================================================================
