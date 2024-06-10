# ===========================================================================
#
# file     : board_luatos_core_esp32c3.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


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
        
        return gf.st7735(
            size = gf.xy( 160, 80 ),
            spi = gf.spi( 
                sck = 2,
                mosi =  3,
                miso = 4,
                mechanism = gf.spi.soft
            ),
            data_command = 6,
            chip_select = 7,
            reset = 10,
            backlight = 11,
            color_order = None if monochrome else "BGR",
            swap_xy = True,
            mirror_x = not rotate,
            mirror_y = rotate,
            offset = gf.xy( 0, 24 )
        )
                
    # =======================================================================
    
    class air101_cursor:
        
        # { 8, 9, 13, 5, 4 }; // UP, RT, DN, LT, CR
        
        def __init__( self ):
            self.pin_north  = gf.gpio_in(  8, pull_up = True ).inverted()
            self.pin_east   = gf.gpio_in(  9, pull_up = True ).inverted()
            self.pin_south  = gf.gpio_in( 13, pull_up = True ).inverted()
            self.pin_west   = gf.gpio_in(  5, pull_up = True ).inverted()
            self.pin_down   = gf.gpio_in(  4, pull_up = True ).inverted()
            
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
            d = gf.xy( 0, 0 )
            if self.north():
                d = d + gf.xy( 0, -1 )
            if self.east():
                d = d + gf.xy( 1, 0 )
            if self.south():
                d = d + gf.xy( 0, 1 )
            if self.west():
                d = d + gf.xy( -1, -0 )                
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
                gf.sleep_us( 500_000 )
                    
    # =======================================================================
        
# ===========================================================================
