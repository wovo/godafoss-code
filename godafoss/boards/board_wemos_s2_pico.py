# ===========================================================================
#
# file     : board_wemos_s2_pico.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

#$$document( 0 )


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
        
        gf.make_pin_out( self.oled_reset ).write( 1 )
        
        return gf.ssd1306(
            size = gf.xy( 128, 32 ),
            spi = self.i2c()
        )
                
    # =======================================================================
        
# ===========================================================================
