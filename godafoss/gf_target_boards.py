# ===========================================================================
#
# file     : gf_board_01space_esp32_c3_042lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the board object for the 01space_esp32_c3_042lcd.
#
# ===========================================================================

from godafoss import *


# ===========================================================================

class badger2040:
    def __init__(
        self
    ) -> None:
        spi = SPI(0, baudrate=12000000, phase=0, polarity=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.display = uc8151(
            spi,
            cs = 17,
            dc = 20,
            rst = 21,
            busy = 26,
            speed = 2,
            no_flickering = False
        )
        
# ===========================================================================



# ===========================================================================

class board_gopherbadge:

    """
    $insert_image( "sunton_wemos_s2_pico", 300 )    

    `manufacturers documentation sunton_sp32_2432s028 board
    <https://www.wemos.cc/en/latest/s2/s2_pico.html>`_

    +-----------+--------------------------------------------------------+
    | uC        | ESP32-S2FNR2 (single core LX7)                         |
    +-----------+--------------------------------------------------------+
    | FLASH     | 4 Mb                                                   |
    +-----------+--------------------------------------------------------+
    | PSRAM     | 2 Mb                                                   |
    +-----------+--------------------------------------------------------+
    | OLED      | SD1306 128 x 32 BW                                     |
    +-----------+--------------------------------------------------------+
    | USB       | C                                                      |
    +-----------+--------------------------------------------------------+
    | LED       | power                                                  |
    +-----------+--------------------------------------------------------+
    | buttons   | boot, reset                                            |
    +-----------+--------------------------------------------------------+
    | misc.     | i2c connector                                          |
    +-----------+--------------------------------------------------------+

    This is an esp32s3 (single core LX7) board with 2 Mb PSRAM, 
    an SD1306 128 x 32 BW OLED, 
    bootload and reset buttons, 
    and an i2c connector.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | button (low when pressed)                                      |
    +-----+----------------------------------------------------------------+
    |  18 | oled_reset                                                     |
    +-----+----------------------------------------------------------------+
    |   9 | i2c_scl                                                        |
    +-----+----------------------------------------------------------------+
    |   8 | i2c_sda                                                        |
    +-----+----------------------------------------------------------------+
    """

    # =======================================================================
       
    def __init__( self ):
        self.led = pin_out( 2 )
        self.neopixels = neopix
        
        self.button = 0

        self.oled_reset = 18
        self.i2c_scl = 9
        self.i2c_sda = 8
          
    # =======================================================================
       
    def i2c(
        self,
        frequency = 100_000
    ):
        import machine
        return machine.SoftI2C(
            freq = frequency,
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        ) 
        
    # =======================================================================

    def display(
        self,
        rotate = False
    ):
        """
        the oled
        
        :param rotate: bool       
        True when the dongle is to be used with
        its USB connector at the right
        """
        
        make_pin_out( self.oled_reset ).write( 1 )
        
        return ssd1306(
            size = xy( 128, 32 ),
            spi = self.i2c()
        )
                
    # =======================================================================
        
# ===========================================================================


# ===========================================================================

class O1space_esp32_c3_042lcd:
    """
    `01space_esp32_c3_042lcd`_ board
    
    .. _01space_esp32_c3_042lcd: https://github.com/01Space/ESP32-C3-0.42LCD
    
    $insert_image( "01space_esp32_c3_042lcd", 1, 300 )
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32-C3                                               |
    +-----------+--------------------------------------------------------+
    | OLED      | SSD1306 74 x 40 monochrome                             |
    +-----------+--------------------------------------------------------+
    | neopixel  | WS2812                                                 |
    +-----------+--------------------------------------------------------+

    This is a very small ESP32 board with a 72 x 40 I2C oled, 
    a single neopixel, and two buttons for bootmode and reset.
    
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | Attribute name                                                 |
    +-----+----------------------------------------------------------------+
    |   2 | neopixel_pin                                                   |
    +-----+----------------------------------------------------------------+
    |   6 | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   5 | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   9 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board 01space_esp32_c3_042lcd
    """
    
    # =======================================================================

    def __init__( self ) -> None:
        self.i2c_scl_pin = 6
        self.i2c_sda_pin = 5
        self.bootmode_pin = 9
        self.neopixel_pin = 2
   
    # =======================================================================

    def i2c( self ) -> "machine.I2C":
        """
        the (soft) I2C bus
        """
        import machine
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl_pin, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda_pin, machine.Pin.OUT )
        ) 
       
    # =======================================================================

    def display( self ) -> "canvas":
        """
        the oled display
        """
        return ssd1306_i2c( 
            size = xy( 72, 40 ), 
            i2c = self.i2c 
        )
        
    # =======================================================================

    def neopixel( self ) -> "canvas":
        """
        the (single) neopixel
        """
        return ws281x( 
            pin = self.neopixel_pin_pin, 
            n = 1
        )
        
    # =======================================================================


# ===========================================================================

class O1space_rp2040_042lcd:
    """
    `01space_rp2040_042lcd`_ board
    
    .. _01space_rp2040_042lcd: https://github.com/01Space/RP2040-0.42LCD
    
    $insert_image( "01space_rp2040_042lcd", 1, 300 )
    
    +-----------+--------------------------------------------------------+
    | uC        | RP2040                                                 |
    +-----------+--------------------------------------------------------+
    | OLED      | SSD1306 74 x 40 monochrome                             |
    +-----------+--------------------------------------------------------+
    | neopixel  | WS2812                                                 |
    +-----------+--------------------------------------------------------+
    | USB       | C                                                      |
    +-----------+--------------------------------------------------------+

    This is a very small RP2040 board with a 72 x 40 I2C oled, 
    a single neopixel, and two buttons for bootmode and reset.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  12 | neopixel_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  23 | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  22 | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  21 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board 01space_rp2040_042lcd
    """

    def __init__( self ):
        self.i2c_scl = 23
        self.i2c_sda = 22
        self.boot = 21
        self.neopixel_pin = 12
   
    def i2c( self ):
        """
        the (soft) I2C bus
        """    
        import machine
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda, machine.Pin.OUT )
        ) 
       
    def display( self ):
        """
        the oled display
        """    
        return ssd1306_i2c( 
            size = xy( 72, 40 ), 
            i2c = self.i2c() 
        )
        
    def neopixel( self ):
        """
        the (single) neopixel
        """    
        return ws281x( 
            pin = self.neopixel_pin, 
            n = 1
        )
    
# ===========================================================================
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
        return sx127x(
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
        gpio_out( self.oled_reset ).write( 1 )    
        return ssd1306_i2c(
            size = xy( 128, 64 ),
            i2c = self.oled_i2c()
        )

        
    # =======================================================================
        
# ===========================================================================
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
    |  35 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |
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
        return st7789(
            size = xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = xy( 51, 40 ),
            x_deadband = 0,
            color_order = None,
            # lookup_table = False
        )
        
    # =======================================================================

    def display( self ):
        """
        the LCD (color driver)
        """        
        return st7789(
            size = xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = xy( 52, 40 )
        )
        
    # =======================================================================
        
# ===========================================================================
# ===========================================================================

class board_lilygo_ttgo_t_display:

    """
    $$insert_image( "lilygo_ttgo_t_display", 300 )
    $$add_board( "boards", "board_lilygo_ttgo_t_display", "lilygo_ttgo_t_display" )
    
    `manufacturers documentation on github x
    <https://github.com/Xinyuan-LilyGO/TTGO-T-Display>`_
    
    +------------------------+-------------------------------------------+
    | uC                     | esp32s3 (dual core)                       |
    +------------------------+-------------------------------------------+
    | Flash                  | W25Q32 8 Mb                               |
    +------------------------+-------------------------------------------+
    | OLED                   | ST7735 0.96" 80 x 160 color               |
    +------------------------+-------------------------------------------+
    | USB                    | A                                         |
    +------------------------+-------------------------------------------+
    | MicroPython free Flash | 8 Mb                                      |
    +------------------------+-------------------------------------------+
    | MicroPython free RAM   | 249088                                    |
    +------------------------+-------------------------------------------+

    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32                                                  |
    +-----------+--------------------------------------------------------+
    | OLED      | ST7789 135 x 240 color                                 |
    +-----------+--------------------------------------------------------+
    | USB       | C, CP2104                                              |
    +-----------+--------------------------------------------------------+
    
    2 Mb
    163712

    This is an ESP32 board with a 135 x 240 SPI color LCD, 
    two input buttons beside the USB connector, 
    and a reset button at the side of the board.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   0 | button2_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  18 | spi_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | spi_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  16 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | tft_rst                                                        |
    +-----+----------------------------------------------------------------+
    |   4 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    """

    # =======================================================================

    def __init__( self ):
    
        self.button1_pin = 35
        self.button1_pin = 0
        
        self.spi_sclk = 18
        self.spi_mosi = 19
        
        self.tft_cs = 5
        self.tft_dc = 16
        self.tft_rst = 23
        self.tft_bl = 4
          
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
        return st7789(
            size = xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = xy( 51, 40 ),
            x_deadband = 0,
            color_order = None,
            # lookup_table = False
        )
        
    # =======================================================================

    def display( self ):
        """
        the LCD (color driver)
        """        
        return st7789(
            size = xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = xy( 52, 40 )
        )
        
    # =======================================================================
        
# ===========================================================================
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
        
        return st7735(
            size = xy( 160, 80 ),
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            swap_xy = True,
            invert = True,
            mirror_y = rotate,
            mirror_x = not rotate,
            offset = xy( 1, 26 ),
            reset = self.tft_rst,
            backlight = make_pin_out( self.tft_bl ).inverted(),
            color_order = None if monochrome else "BGR",
        )
                
    # =======================================================================
        
    def neopixel( self ):
        """
        the single neopixel
        """        
        
        return apa102(
            n = 1, 
            ci = self.led_ci,
            di = self.led_di,
        )
        
    # =======================================================================
        
# ===========================================================================
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
        make_pin_out( self.tft_rst ).write( 1 )
        return st7735(
            size = xy( 128, 128 ),
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            swap_xy = True,
            invert = True,
            mirror_y = rotate,
            mirror_x = not rotate,
            offset = xy( 1, 2 ),
            reset = self.tft_rst,
            backlight = make_pin_out( self.tft_bl ).inverted(),
            color_order = None if monochrome else "BGR",
        )
        
    # =======================================================================
        
# ===========================================================================
# ===========================================================================

class board_lilygo_ttgo_t_qt_v11:

    """
    `lilygo_ttgo_t_qt_v11`_ watch
    
    .. _lilygo_ttgo_t_qt_v11: \\
        https://github.com/Xinyuan-LilyGO/T-Wristband
        
http://www.lilygo.cn/prod_view.aspx?TypeId=50054&Id=1314&FId=t3:50054:3        
    
    $insert_image( "lilygo_ttgo_t_wristband", 1, 300 )
    
    +-----------------+-----------------------------------------------------+
    | uC              | ESP32-S3                                            |
    +-----------------+-----------------------------------------------------+
    | LCD             | GC9107 18 x 128 color                               |
    +-----------------+-----------------------------------------------------+
    | USB             | C, CH340, boot / reset buttons                      |
    +-----------------+-----------------------------------------------------+

    This is an wrist watch with an ESP32 with PSRAM, a small LiPo accu,
    a touch LCD, a vibration/buzzer motor, an accelerometer, 
    i2s audio with a small speaker, and an RTC.
    
    Pressing the button on the side for 5 seconds powers the watch down.
    When powered down, pressing it for 2 seconds restarts it.
    If this button can be read by the ESP32 I have not found out how.
    
    The names in the table below are available as attributes.    

    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  18 | i2c_sda (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  19 | i2c_scl (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  35 | power_int_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  39 | accelerometer_int_pin                                          |
    +-----+----------------------------------------------------------------+
    |  18 | tft_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | tft_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  27 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  12 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | touch_i2c_sda                                                  |
    +-----+----------------------------------------------------------------+
    |  32 | touch_i2c_scl                                                  |
    +-----+----------------------------------------------------------------+
    |  38 | touch_int                                                      |
    +-----+----------------------------------------------------------------+
    |  25 | audio_i2s_ws                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | audio_i2s_bck                                                  |
    +-----+----------------------------------------------------------------+
    |  33 | audio_i2s_dout                                                 |
    +-----+----------------------------------------------------------------+
    |   4 | buzzer_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  13 | ir_pin                                                         |
    +-----+----------------------------------------------------------------+
    |  37 | rtc_pin                                                        |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_wristband
    """

    # =======================================================================

    def __init__( self ):
    
        self.i2c_sda = 21
        self.i2c_scl = 22
        self.power_int_pin = 35
        self.accelerometer_int_pin = 39
        
        self.tft_sclk = 18
        self.tft_mosi = 19
        self.tft_cs = 5
        self.tft_dc = 23
        self.tft_rst = 26
        self.tft_bl = 27
        
        self.touch_i2c_sda = 23
        self.touch_i2c_scl = 32
        self.touch_int = 38
        
        self.audio_i2s_ws = 25
        self.audio_i2s_bck = 26
        self.audio_is2_dout = 33
        
        self.buzzer_pin = 4
        self.ir_pin = 13        
        self.rtc_pin = 37
        
        self.power_i2c_address = 0x35
        self.accelerometer_i2c_address = 0x18
        
        self._i2c = None
       
          
    # =======================================================================
       
    def display_spi( 
        self, 
        id: int = 1,
        baudrate = 30_000_000,
        polarity = 1,
        phase = 1       
    ) -> "machine.SPI":
        """
        default (hard) SPI bus for the LCD
        """
        
        import machine
        return machine.SPI(
            id,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( 23 ) # dummy
        )
        
    # =======================================================================

    def display( 
        self,
        spi: "machine.SPI" = None
    ) -> canvas:
        """
        ST7789 240 x 240 color LCD
        
        After a restart the LCD is disabled and the backlight is off.
        The display constructor enables the LCD 
        and switches the backlight on.        
        """          

        return st7735( 
            size = xy( 160, 80 ), 
            spi = spi if spi is not None else self.display_spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            invert = True,
        )
        
    # =======================================================================
    
    def i2c( self ) -> "machine.I2C":
        """
        i2c bus for the power and accelerometer
        
        This function returns the i2c bus for the AXP202 power
        management chip and the BMA423 accelerometer.
        """        
        
        if self._i2c is None:
            self._i2c = machine.SoftI2C(
                scl = machine.Pin( self.i2c_scl ),
                sda  = machine.Pin( self.i2c_sda ),
                freq = 100_000
            )    
        return self._i2c

    # =======================================================================
    
    def display_enable( self ) -> None:
        """
        enable power to the LCD
        """
        
        i2c = self.i2c()  
        power_output_control = i2c.readfrom_mem( 
            self.power_i2c_address, 
            0x12, 
            1 
        )[ 0 ]
        power_output_control |= 4 # LDO2 enable
        i2c.writeto_mem( 
            self.power_i2c_address, 
            0x12, 
            bytes( [ power_output_control ] ) 
        )        
    
    # =======================================================================
    
    def touch_i2c( 
        self, 
        freq: int = 100_000 
    ) -> "machine.I2C":
        """
        touch chip i2c bus
        """
        
        import machine
        return machine.SoftI2C(
            scl = machine.Pin( self.touch_i2c_scl ),
            sda = machine.Pin( self.touch_i2c_sda ),
            freq = freq
        ) 
        
    # =======================================================================
    
    def touch( 
        self,
        i2c: "machine.I2C" = None
    ):
        """
        ft6236 touch chip
        """

        return ft6236( i2c if i2c is not None else self.touch_i2c() )
    
    # =======================================================================
    
    def buzzer( self ) -> pin_out:
        """
        buzzer pin
        """

        return make_pin_out( self.buzzer_pin )
        
    # =======================================================================

# ===========================================================================
# ===========================================================================

class board_lilygo_ttgo_t_watch_2020:

    """
    `lilygo_ttgo_t_watch_2020`_ watch
    
    .. _lilygo_ttgo_t_watch_2020: \\
        https://t-watch-document-en.readthedocs.io\\
        /en/latest/introduction/product/2020.html
    
    $insert_image( "lilygo_ttgo_t_watch_2020", 1, 300 )
    
    +-----------------+-----------------------------------------------------+
    | uC              | ESP32 with PSRAM                                    |
    +-----------------+-----------------------------------------------------+
    | LCD             | ST7789 240 x 240 color                              |
    +-----------------+-----------------------------------------------------+
    | Touch           | FT6236                                              |
    +-----------------+-----------------------------------------------------+
    | Power           | AXP202                                              |
    +-----------------+-----------------------------------------------------+
    | Audio           | MAX98357A                                           |
    +-----------------+-----------------------------------------------------+
    | Accelerometer   | BMA423                                              |
    +-----------------+-----------------------------------------------------+
    | Real Time Clock | PCF8563                                             |
    +-----------------+-----------------------------------------------------+
    | USB             | micro, CH9102, boot / reset circuit                 |
    +-----------------+-----------------------------------------------------+

    This is an wrist watch with an ESP32 with PSRAM, a small LiPo accu,
    a touch LCD, a vibration/buzzer motor, an accelerometer, 
    i2s audio with a small speaker, and an RTC.
    
    Pressing the button on the side for 5 seconds powers the watch down.
    When powered down, pressing it for 2 seconds restarts it.
    If this button can be read by the ESP32 I have not found out how.
    
    The names in the table below are available as attributes.    

    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  18 | i2c_sda (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  19 | i2c_scl (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  35 | power_int_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  39 | accelerometer_int_pin                                          |
    +-----+----------------------------------------------------------------+
    |  18 | tft_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | tft_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  27 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  12 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | touch_i2c_sda                                                  |
    +-----+----------------------------------------------------------------+
    |  32 | touch_i2c_scl                                                  |
    +-----+----------------------------------------------------------------+
    |  38 | touch_int                                                      |
    +-----+----------------------------------------------------------------+
    |  25 | audio_i2s_ws                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | audio_i2s_bck                                                  |
    +-----+----------------------------------------------------------------+
    |  33 | audio_i2s_dout                                                 |
    +-----+----------------------------------------------------------------+
    |   4 | buzzer_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  13 | ir_pin                                                         |
    +-----+----------------------------------------------------------------+
    |  37 | rtc_pin                                                        |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_watch_2020
    """

    # =======================================================================

    def __init__( self ):
    
        self.i2c_sda = 21
        self.i2c_scl = 22
        self.power_int_pin = 35
        self.accelerometer_int_pin = 39
        
        self.tft_sclk = 18
        self.tft_mosi = 19
        self.tft_cs = 5
        self.tft_dc = 27
        self.tft_bl = 12
        
        self.touch_i2c_sda = 23
        self.touch_i2c_scl = 32
        self.touch_int = 38
        
        self.audio_i2s_ws = 25
        self.audio_i2s_bck = 26
        self.audio_is2_dout = 33
        
        self.buzzer_pin = 4
        self.ir_pin = 13        
        self.rtc_pin = 37
        
        self.power_i2c_address = 0x35
        self.accelerometer_i2c_address = 0x18
        
        self._i2c = None
       
          
    # =======================================================================
       
    def display_spi( 
        self, 
        id: int = 1,
        baudrate = 30_000_000,
        polarity = 1,
        phase = 1       
    ) -> "machine.SPI":
        """
        default (hard) SPI bus for the LCD
        """
        
        import machine
        return machine.SPI(
            id,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( 23 ) # dummy
        )
        
    # =======================================================================

    def display( 
        self,
        spi: "machine.SPI" = None
    ) -> canvas:
        """
        ST7789 240 x 240 color LCD
        
        After a restart the LCD is disabled and the backlight is off.
        The display constructor enables the LCD 
        and switches the backlight on.        
        """          
        self.display_enable()
        return st7789( 
            size = xy( 240, 240 ), 
            spi = spi if spi is not None else self.display_spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            backlight = self.tft_bl,
            invert = True,
        )
        
    # =======================================================================
    
    def i2c( self ) -> "machine.I2C":
        """
        i2c bus for the power and accelerometer
        
        This function returns the i2c bus for the AXP202 power
        management chip and the BMA423 accelerometer.
        """        
        
        if self._i2c is None:
            self._i2c = machine.SoftI2C(
                scl = machine.Pin( self.i2c_scl ),
                sda  = machine.Pin( self.i2c_sda ),
                freq = 100_000
            )    
        return self._i2c

    # =======================================================================
    
    def display_enable( self ) -> None:
        """
        enable power to the LCD
        """
        
        i2c = self.i2c()  
        power_output_control = i2c.readfrom_mem( 
            self.power_i2c_address, 
            0x12, 
            1 
        )[ 0 ]
        power_output_control |= 4 # LDO2 enable
        i2c.writeto_mem( 
            self.power_i2c_address, 
            0x12, 
            bytes( [ power_output_control ] ) 
        )        
    
    # =======================================================================
    
    def touch_i2c( 
        self, 
        freq: int = 100_000 
    ) -> "machine.I2C":
        """
        touch chip i2c bus
        """
        
        return machine.SoftI2C(
            scl = machine.Pin( self.touch_i2c_scl ),
            sda = machine.Pin( self.touch_i2c_sda ),
            freq = freq
        ) 
        
    # =======================================================================
    
    def touch( 
        self,
        i2c: "machine.I2C" = None
    ):
        """
        ft6236 touch chip
        """

        return ft6236( i2c if i2c is not None else self.touch_i2c() )
    
    # =======================================================================
    
    def buzzer( self ) -> pin_out:
        """
        buzzer pin
        """

        return pin_out( self.buzzer_pin )
        
    # =======================================================================


# ===========================================================================

class board_lilygo_ttgo_t_wristband:

    """
    `lilygo_ttgo_t_wristband`_ watch
    
    .. _lilygo_ttgo_t_wristband: \\
        https://github.com/Xinyuan-LilyGO/T-Wristband
        
http://www.lilygo.cn/prod_view.aspx?TypeId=50054&Id=1314&FId=t3:50054:3        
    
    $insert_image( "lilygo_ttgo_t_wristband", 1, 300 )
    
    +-----------------+-----------------------------------------------------+
    | uC              | ESP32 with PSRAM                                    |
    +-----------------+-----------------------------------------------------+
    | LCD             | ST7789 240 x 240 color                              |
    +-----------------+-----------------------------------------------------+
    | Touch           | FT6236                                              |
    +-----------------+-----------------------------------------------------+
    | Power           | AXP202                                              |
    +-----------------+-----------------------------------------------------+
    | Audio           | MAX98357A                                           |
    +-----------------+-----------------------------------------------------+
    | Accelerometer   | BMA423                                              |
    +-----------------+-----------------------------------------------------+
    | Real Time Clock | PCF8563                                             |
    +-----------------+-----------------------------------------------------+
    | USB             | (on the breakout board:)                            |
    |                 | C & micro, CH340, boot / reset buttons              |
    +-----------------+-----------------------------------------------------+

    This is an wrist watch with an ESP32 with PSRAM, a small LiPo accu,
    a touch LCD, a vibration/buzzer motor, an accelerometer, 
    i2s audio with a small speaker, and an RTC.
    
    Pressing the button on the side for 5 seconds powers the watch down.
    When powered down, pressing it for 2 seconds restarts it.
    If this button can be read by the ESP32 I have not found out how.
    
    The names in the table below are available as attributes.    

    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  18 | i2c_sda (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  19 | i2c_scl (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  35 | power_int_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  39 | accelerometer_int_pin                                          |
    +-----+----------------------------------------------------------------+
    |  18 | tft_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | tft_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  27 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  12 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | touch_i2c_sda                                                  |
    +-----+----------------------------------------------------------------+
    |  32 | touch_i2c_scl                                                  |
    +-----+----------------------------------------------------------------+
    |  38 | touch_int                                                      |
    +-----+----------------------------------------------------------------+
    |  25 | audio_i2s_ws                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | audio_i2s_bck                                                  |
    +-----+----------------------------------------------------------------+
    |  33 | audio_i2s_dout                                                 |
    +-----+----------------------------------------------------------------+
    |   4 | buzzer_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  13 | ir_pin                                                         |
    +-----+----------------------------------------------------------------+
    |  37 | rtc_pin                                                        |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_wristband
    """

    # =======================================================================

    def __init__( self ):
    
        self.i2c_sda = 21
        self.i2c_scl = 22
        self.power_int_pin = 35
        self.accelerometer_int_pin = 39
        
        self.tft_sclk = 18
        self.tft_mosi = 19
        self.tft_cs = 5
        self.tft_dc = 23
        self.tft_rst = 26
        self.tft_bl = 27
        
        self.touch_i2c_sda = 23
        self.touch_i2c_scl = 32
        self.touch_int = 38
        
        self.audio_i2s_ws = 25
        self.audio_i2s_bck = 26
        self.audio_is2_dout = 33
        
        self.buzzer_pin = 4
        self.ir_pin = 13        
        self.rtc_pin = 37
        
        self.power_i2c_address = 0x35
        self.accelerometer_i2c_address = 0x18
        
        self._i2c = None
       
          
    # =======================================================================
       
    def display_spi( 
        self, 
        id: int = 1,
        baudrate = 30_000_000,
        polarity = 1,
        phase = 1       
    ) -> "machine.SPI":
        """
        default (hard) SPI bus for the LCD
        """
        
        import machine
        return machine.SPI(
            id,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( 23 ) # dummy
        )
        
    # =======================================================================

    def display( 
        self,
        spi: "machine.SPI" = None
    ) -> canvas:
        """
        ST7789 240 x 240 color LCD
        
        After a restart the LCD is disabled and the backlight is off.
        The display constructor enables the LCD 
        and switches the backlight on.        
        """          

        return st7735( 
            size = xy( 160, 80 ), 
            spi = spi if spi is not None else self.display_spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            invert = True,
        )
        
    # =======================================================================
    
    def i2c( self ) -> "machine.I2C":
        """
        i2c bus for the power and accelerometer
        
        This function returns the i2c bus for the AXP202 power
        management chip and the BMA423 accelerometer.
        """        
        
        import machine
        if self._i2c is None:
            self._i2c = machine.SoftI2C(
                scl = machine.Pin( self.i2c_scl ),
                sda  = machine.Pin( self.i2c_sda ),
                freq = 100_000
            )    
        return self._i2c

    # =======================================================================
    
    def display_enable( self ) -> None:
        """
        enable power to the LCD
        """
        
        i2c = self.i2c()  
        power_output_control = i2c.readfrom_mem( 
            self.power_i2c_address, 
            0x12, 
            1 
        )[ 0 ]
        power_output_control |= 4 # LDO2 enable
        i2c.writeto_mem( 
            self.power_i2c_address, 
            0x12, 
            bytes( [ power_output_control ] ) 
        )        
    
    # =======================================================================
    
    def touch_i2c( 
        self, 
        freq: int = 100_000 
    ) -> "machine.I2C":
        """
        touch chip i2c bus
        """
        
        return machine.SoftI2C(
            scl = machine.Pin( self.touch_i2c_scl ),
            sda = machine.Pin( self.touch_i2c_sda ),
            freq = freq
        ) 
        
    # =======================================================================
    
    def touch( 
        self,
        i2c: "machine.I2C" = None
    ):
        """
        ft6236 touch chip
        """

        return ft6236( i2c if i2c is not None else self.touch_i2c() )
    
    # =======================================================================
    
    def buzzer( self ) -> pin_out:
        """
        buzzer pin
        """

        return pin_out( self.buzzer_pin )
        
    # =======================================================================


# ===========================================================================

class board_lolin_s2_pico:

    # =======================================================================

    def __init__( self ):
        self.button1_pin = 35
        
    # =======================================================================

    def display( self ): 
        import machine
        return ssd1306_i2c(
            xy( 128, 32 ),
            machine.SoftI2C(
                scl = machine.Pin( 9 ),
                sda = machine.Pin( 8 )
            )    
        )
        
    # =======================================================================
        
# ===========================================================================
# ===========================================================================

class board_luatos_core_esp32c3:

    """
    $insert_image( "luatos_core_esp32c3", 00 ) 
    $$add_table( "boards", "board_luatos_core_esp32c3", "luatos_core_esp32c3" )
    
    `manufacturers documentation
    <https://wiki.luatos.org/chips/esp32c3/board.html>`_
    

    +------------------------+----------------------------------------------+
    | uC                     | ESP32-C3 (dual core LX7)                     |
    +------------------------+----------------------------------------------+
    | FLASH                  | 4 Mb                                         |
    +------------------------+----------------------------------------------+
    | USB                    | C                                            |
    +------------------------+----------------------------------------------+
    | LED                    | 2                                            |
    +------------------------+----------------------------------------------+
    | buttons                | boot, reset                                  |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 2 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 200160                                       |
    +------------------------+----------------------------------------------+
    
    This is an esp32c3 (dual core LX7) board with 
    2 LEDs, and 
    bootload and reset buttons.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   9 | button (low when pressed)                                      |
    +-----+----------------------------------------------------------------+
    |  12 | led_1                                                          |
    +-----+----------------------------------------------------------------+
    |  13 | led_2                                                          |
    +-----+----------------------------------------------------------------+

    The Air-101 board has a matching pinout so it can be 
    combined directly with the esp32c3 board.
    It has an ST7735 160 * 80 color LCD and a 5 switch cursor.
    
    $insert_image( "luatos_core_esp32c3_air101_python" 1, 300)        

    """

    # =======================================================================
       
    def __init__( self ):
        self.button = 0

        self.button = 9
        self.led_1 = 12
        self.led_2 = 13
          
    # =======================================================================
       
    def i2c(
        self,
        frequency = 100_000
    ):
        import machine
        return machine.SoftI2C(
            freq = frequency,
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        ) 
        
    # =======================================================================

    def air101_display(
        self,
        rotate = False,
        monochrome = False
    ):
        """
        a connected air101 display

        :param rotate: bool       
            True when the combo is to be used with
            its USB connector at the left

        :param monochrome: bool        
            True to use the display in monochrome mode        
        """
        
        return st7735(
            size = xy( 160, 80 ),
            spi = spi( 
                sck = 2,
                mosi =  3,
                miso = 4,
                mechanism = spi.soft
            ),
            data_command = 6,
            chip_select = 7,
            reset = 10,
            backlight = 11,
            color_order = None if monochrome else "BGR",
            swap_xy = True,
            mirror_x = not rotate,
            mirror_y = rotate,
            offset = xy( 0, 24 )
        )
                
    # =======================================================================
    
    class air101_cursor:
        
        # { 8, 9, 13, 5, 4 }; // UP, RT, DN, LT, CR
        
        def __init__( self ):
            self.pin_north  = gpio_in(  8, pull_up = True ).inverted()
            self.pin_east   = gpio_in(  9, pull_up = True ).inverted()
            self.pin_south  = gpio_in( 13, pull_up = True ).inverted()
            self.pin_west   = gpio_in(  5, pull_up = True ).inverted()
            self.pin_down   = gpio_in(  4, pull_up = True ).inverted()
            
        def north( self ):
            return self.pin_north.read()
        
        def east( self ):
            return self.pin_east.read()
        
        def south( self ):
            return self.pin_south.read()
        
        def west( self ):
            return self.pin_west.read()
        
        def down( self ):
            return self.pin_down.read()
        
        def direction( self ):
            d = xy( 0, 0 )
            if self.north():
                d = d + xy( 0, -1 )
            if self.east():
                d = d + xy( 1, 0 )
            if self.south():
                d = d + xy( 0, 1 )
            if self.west():
                d = d + xy( -1, -0 )                
            return d   
        
        def demo( self ):
            while True:
                s = ""
                for name, pin in (
                    ( "n", self.north ),
                    ( "e", self.east ),
                    ( "s", self.south ),
                    ( "w", self.west ),
                    ( "down", self.down ),
                ):
                    s += f"{name}={pin()} "
                print( s )
                sleep_us( 500_000 )
                    
    # =======================================================================
        
# ===========================================================================
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
        spi = spi(
            id = 1,
            frequency = 30_000_000,
            sck = self.lcd_sclk_pin,
            mosi = self.lcd_mosi_pin,
            miso = 15 # dummy
        )        
        return st7789(
            size = xy( 320, 170 ) if horizontal else xy( 170, 320 ), 
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
            offset = xy( 0, 35 ) if horizontal else xy( 35, 0 )
        )
        
# ===========================================================================
# ===========================================================================

class board_sunton_esp32_2432s028:

    """
    $insert_image( "sunton_esp32_2432s028_python", 1, 200, width = 45 )
    $insert_image( "sunton_esp32_2432s028_back", 1, 200, width = 45 )
    
    `manufacturers documentation (zip)
    <http://pan.jczn1688.com/directlink/1/ESP32%20module/1.9inch_ESP32-1732S019.zip>`_
    
    +------------------------+----------------------------------------------+
    | uC                     | esp32 (dual core)                            |
    +------------------------+----------------------------------------------+
    | Flash                  | 4 Mb                                         |
    +------------------------+----------------------------------------------+
    | SPIRAM (octal)         | 8 Mb                                         |
    +------------------------+----------------------------------------------+
    | LCD                    | ST7789 1.9" 320 x 170 color                  |
    +------------------------+----------------------------------------------+
    | USB                    | C, CH340, boot & reset circuit,              |
    |                        | linear regulator                             |
    +------------------------+----------------------------------------------+
    | MicroPython free Flash | 2 Mb                                         |
    +------------------------+----------------------------------------------+
    | MicroPython free RAM   | 163712 (without SPIRAM)                      |
    |                        | xxx (with SPIRAM)                            |
    +------------------------+----------------------------------------------+     
    
    163712
    
    sunton_sp32_2432s028 board
    
    
    $insert_image( "sunton_esp32_2432s028_front", 1, 200, width = 45 )
    $insert_image( "sunton_esp32_2432s028_back", 1, 200, width = 45 )
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32                                                  |
    +-----------+--------------------------------------------------------+
    | LCD       | ILI9341 240 * 430 color                                |
    +-----------+--------------------------------------------------------+
    | touch     | XPT2046 (resistive)                                    |
    +-----------+--------------------------------------------------------+
    | USB       | micro, CH340, boot & reset circuit,                    |
    |           | linear regulator                                       |
    +-----------+--------------------------------------------------------+
    | LED       | RGB leds                                               |
    +-----------+--------------------------------------------------------+
    | Sound     | filter, SC8002B 3W aplifier, 2 pin connector           |
    +-----------+--------------------------------------------------------+
    | LDR       | analog input                                           |
    +-----------+--------------------------------------------------------+
    | buttons   | boot, reset                                            |
    +-----------+--------------------------------------------------------+
    | misc.     | boot & reset buttons, SD card,                         |
    |           | connector, single-wire connector                       |
    +-----------+--------------------------------------------------------+

    This is an ESP32 board with a color LCD with touch, RGB leds,
    buttons for bootmode and reset, a LiPo connector and
    simple charge circuit (with linear regulators), a speaker interface,
    
    without spiram, the display can't be used in color mode
    
    PSRAM??
    
    The names in the table below are available as attributes.
    Note that the touch chip, the LCD and the SD card use separate
    SPI busses.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   4 | red_led_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  16 | green_led_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  17 | blue_led_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | speaker_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  34 | ldr_pin                                                        |
    +-----+----------------------------------------------------------------+
    |  14 | tft_sclk_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  13 | tft_mosi_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  12 | tft_miso_pin                                                   |
    +-----+----------------------------------------------------------------+
    |   2 | tft_rs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  15 | tft_cs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |     | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |     | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  21 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board sunton_esp32_2432s028
    
    http://www.jczn1688.com/zlxz
    """


    def __init__( self ):
        
        self.red_led_pin = 4
        self.green_led_pin = 16
        self.blue_led_pin = 17
        
        self.speaker_pin = 26
        self.ldr_pin = 34
        self.boot_pin = 0        
   
        self.touch_sclk = 25
        self.touch_mosi = 32
        self.touch_miso = 39
        self.touch_cs = 33
        self.touch_irq = 36
        
        self.tft_sclk = 14
        self.tft_mosi = 13
        self.tft_miso = 12
        self.tft_rs = 2
        self.tft_cs = 15
        self.tft_bl = 21
                 
        self.sd_sclk = 18
        self.sd_mosi = 23
        self.sd_miso = 19
        self.sd_cs = 5
        
    def touch( self ):
        spi = machine.SoftSPI( 
            baudrate = 10_000,
            sck = machine.Pin( self.touch_sclk ),
            mosi = machine.Pin( self.touch_mosi ),
            miso = machine.Pin( self.touch_miso )
        )
        return xpt2046(
            spi = spi,
            cs = self.touch_cs
        )        
        
    def display( self ):
        import machine
        spi = machine.SPI(
            1,
            baudrate = 30_000,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( self.tft_miso )
        )        
        return ili9341(
            size = xy( 240, 320 ), 
            spi = spi,
            data_command = self.tft_rs,
            chip_select = self.tft_cs,
            backlight = self.tft_bl,
            color_order = "RGB",
            mechanism = 0
        )
        
    def display_monochrome( self ):
        spi = machine.SPI(
            1,
            baudrate = 30_000,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( self.tft_miso )
        )        
        return ili9341(
            size = xy( 240, 320 ), 
            spi = spi,
            data_command = self.tft_rs,
            chip_select = self.tft_cs,
            backlight = self.tft_bl,
            color_order = None,
            mechanism = 0
        )
        
# ===========================================================================
# ===========================================================================

class board_ttgo_txx_display:

    """
    https://www.waveshare.com/rp2040-lcd-0.96.htm
    
    should use hard spi
    """

    def __init__( self ):
   
        self.i2c_scl = 21
        self.i2c_sda = 22
        
        self.spi_miso = 2 # dummy
        self.spi_mosi = 19
        self.spi_sclk = 18
        
        self.tft_cs = 5
        self.tft_dc = 16
        self.tft_rst = 23
        self.tft_bl = 4
        
        self.button1 = 35
        self.button2 = 0
        
    def i2c( self ):
        import machine
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda, machine.Pin.OUT )
        ) 
        
    def spi( 
        self, 
        baudrate = 10_000_000,
        polarity = 1,
        phase = 1       
    ):
        import machine    
        return machine.SoftSPI( 
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sclk, machine.Pin.OUT ),
            mosi = machine.Pin( self.spi_mosi, machine.Pin.OUT ),
            miso = machine.Pin( self.spi_miso, machine.Pin.IN )
        )
        
    def display( self ):
        return st7789_monochrome( 
            size = xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            offset = xy( 52, 40 )
        )
        
# ===========================================================================
# ===========================================================================

class board_wemos_s2_pico:

    """
    $insert_image( "sunton_wemos_s2_pico", 300 )    

    `manufacturers documentation sunton_sp32_2432s028 board
    <https://www.wemos.cc/en/latest/s2/s2_pico.html>`_

    +-----------+--------------------------------------------------------+
    | uC        | ESP32-S2FNR2 (single core LX7)                         |
    +-----------+--------------------------------------------------------+
    | FLASH     | 4 Mb                                                   |
    +-----------+--------------------------------------------------------+
    | PSRAM     | 2 Mb                                                   |
    +-----------+--------------------------------------------------------+
    | OLED      | SD1306 128 x 32 BW                                     |
    +-----------+--------------------------------------------------------+
    | USB       | C                                                      |
    +-----------+--------------------------------------------------------+
    | LED       | power                                                  |
    +-----------+--------------------------------------------------------+
    | buttons   | boot, reset                                            |
    +-----------+--------------------------------------------------------+
    | misc.     | i2c connector                                          |
    +-----------+--------------------------------------------------------+

    This is an esp32s3 (single core LX7) board with 2 Mb PSRAM, 
    an SD1306 128 x 32 BW OLED, 
    bootload and reset buttons, 
    and an i2c connector.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | button (low when pressed)                                      |
    +-----+----------------------------------------------------------------+
    |  18 | oled_reset                                                     |
    +-----+----------------------------------------------------------------+
    |   9 | i2c_scl                                                        |
    +-----+----------------------------------------------------------------+
    |   8 | i2c_sda                                                        |
    +-----+----------------------------------------------------------------+
    """

    # =======================================================================
       
    def __init__( self ):
        self.button = 0

        self.oled_reset = 18
        self.i2c_scl = 9
        self.i2c_sda = 8
          
    # =======================================================================
       
    def i2c(
        self,
        frequency = 100_000
    ):
        import machine
        return machine.SoftI2C(
            freq = frequency,
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        ) 
        
    # =======================================================================

    def display(
        self,
        rotate = False
    ):
        """
        the oled
        
        :param rotate: bool       
        True when the dongle is to be used with
        its USB connector at the right
        """
        
        make_pin_out( self.oled_reset ).write( 1 )
        
        return ssd1306(
            size = xy( 128, 32 ),
            spi = self.i2c()
        )
                
    # =======================================================================
        
# ===========================================================================

