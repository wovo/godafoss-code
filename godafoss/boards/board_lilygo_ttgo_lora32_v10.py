# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_lora32_v10.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class board_lilygo_ttgo_lora32_v10:

    """
    `lilygo_ttgo_lora32_v10`_ board
    
    .. _lilygo_ttgo_lora32_v10: \\
        https://www.lilygo.cc/products/lora32-v1-0
        
    .. github: \\
        https://github.com/Xinyuan-LilyGO/TTGO-LoRa-Series      
    
    $insert_image( "https://www.lilygo.cc/products/lora32-v1-0", 1, 300 )
    
    +------------------------+----------------------------------------------+
    | uC                     | ESP32-D0WDQ6, 4Mb FLASH                      |
    +------------------------+----------------------------------------------+
    | Flash                  | 4 Mb                                         |
    +------------------------+----------------------------------------------+
    | WiFi                   | ESP32, onboard antenna                       |
    +------------------------+----------------------------------------------+
    | LoRa                   | SX1276, UPEX antenna connector               |
    +------------------------+----------------------------------------------+
    | OLED                   | SSD1306 128*64 0.96"                         |
    +------------------------+----------------------------------------------+
    | USB                    | micro, CH910X                                |
    +------------------------+----------------------------------------------+
    | LiPo                   | TP4054, 2 pin molex                          |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 2 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 163120                                       |
    +------------------------+----------------------------------------------+
    
    This is an ESP32 board with an SX1276 Lora chip,
    128 * 64 monochrome OLED, boot and reset buttons, and a single blue LED.
    It has micro USB connector with a CH910X USB-to-serial converter.
    The names in the table below are available as attributes.
    
    +-----+-----------------------------------------------------------------+
    | Pin | name                                                            |
    +-----+-----------------------------------------------------------------+
    |   4 | oled_i2c_sda                                                    |
    +-----+-----------------------------------------------------------------+
    |  15 | oled_i2c_scl                                                    |
    +-----+-----------------------------------------------------------------+
    |  16 | oled_reset (low to reset)                                       |
    +-----+-----------------------------------------------------------------+
    |  27 | lora_spi_mosi                                                   |
    +-----+-----------------------------------------------------------------+
    |  19 | lora_spi_miso                                                   |
    +-----+-----------------------------------------------------------------+
    |   5 | lora_spi_sclk                                                   |
    +-----+-----------------------------------------------------------------+
    |  18 | lora_spi_cs                                                     |
    +-----+-----------------------------------------------------------------+
    |  14 | lora_rst                                                        |
    +-----+-----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_display
    """

    # =======================================================================

    def __init__( self ):
    
        self.led = 25
        
        self.oled_i2c_scl = 15
        self.oled_i2c_sda = 4
        self.oled_reset = 16
        
        self.lora_spi_mosi = 27
        self.lora_spi_miso = 19
        self.lora_spi_sclk = 5
        self.lora_spi_cs = 18
        self.lora_reset = 14
          
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
            sck = machine.Pin( self.lora_spi_sclk ),
            mosi = machine.Pin( self.lora_spi_mosi ),

            # dummy, the default MISO pin is used for the tft_rst
            miso = machine.Pin( self.lora_spi_miso )
        )
        
    # =======================================================================
    
    def lora( 
        self,
        configuration = None
    ):
        return gf.sx127x(
            spi = self.spi(),
            chip_select = self.lora_spi_cs,
            configuration = configuration,
        )
    
    # =======================================================================
    
    def oled_i2c( self ):
        return machine.SoftI2C(
            scl = machine.Pin( self.oled_i2c_scl ),
            sda = machine.Pin( self.oled_i2c_sda )
        ) 

    # =======================================================================

    def display( self ):
        """
        """        
        gf.gpio_out( self.oled_reset ).write( 1 )    
        return gf.ssd1306_i2c(
            size = gf.xy( 128, 64 ),
            i2c = self.oled_i2c()
        )

        
    # =======================================================================
        
# ===========================================================================
