# ===========================================================================
#
# file     : generic_color_lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license  (from license.py)
#
# ===========================================================================

from godafoss import *

    
# ===========================================================================

class lcd_reset_backlight_power:
    """
    lcd common functionality
    
    :param rst: (None, int, pin_out, pin_in_out, pin_oc)
        reset pin; active low; high for normal operation

    :param bl: (None, int, pin_out, pin_in_out, pin_oc)
        backlight pin; active high

    :param power: (None, int, pin_out, pin_in_out, pin_oc)
        power pin, active high

    :param reset_duration: (int)
        width of a reset pulse, in microseconds (default 1)

    :param reset_wait: (int)
        wait time after a reset, in microseconds (default 1)

    This class provides the basic functions for a typical LCD
    of having reset, backlight and power pins.
    All pins are optional, and active high.    .
    The constructor enables power and backlight, 
    and resets the lcd.
    
    $macro_start lcd_reset_backlight_power_parameters
    
    :param reset: ($macro_insert make_pin_out_types)
        reset pin (optional), active low, high for normal operation
        
    :param backlight: ($macro_insert make_pin_out_types)
        backlight pin (optional), active high
        
    :param power: ($macro_insert make_pin_out_types)
        power pin (optional), active high   
        
    $macro_end
    
    $macro_start lcd_reset_backlight_power_functionality
    This class inherits from 
    :class:`~godafoss:lcd_reset_backlight_power`, 
    which provides functions to reset, switch the power, 
    and switch the backlight
    (when the respective pins are available).
    $macro_end
    """

    # =======================================================================

    def __init__(
        self, 
        reset: [ None, int, gf.can_pin_out ],
        backlight: [ None, int, gf.can_pin_out ],
        power: [ None, int, gf.can_pin_out ],
        reset_duration: int = 1_000,
        reset_wait: int = 1_000
    ) -> None:
        self._reset = gf.pin_out( reset )
        self._backlight = gf.pin_out( backlight )
        self._power = gf.pin_out( power )
        self._reset_duration = reset_duration
        self._reset_wait = reset_wait
    
        self.power( 1 )
        self.backlight( 1 )
        self.reset()
        
    # =======================================================================

    def reset( self ) -> None:
        """
        hard-reset the display.
        """
        
        self._reset.pulse( 
            self._reset_duration, 
            self._reset_wait 
        )          
        
    # =======================================================================

    def backlight(
        self,
        state: bool
    ) -> None:
        """
        turn the backlight on (True) or off (False)
        """
        
        self._backlight.write( state )
        
    # =======================================================================

    def backlight_blink(
        self,
        high_time = 500_000,
        low_time = None,        
        iterations: None = None,
        
    ):
        for _ in gf.repeater( iterations ):
            self.backlight( 1 )
            gf.sleep_us( high_time )
            self.backlight( 0 )
            gf.sleep_us( first_not_none( low_time, high_time ) )        
        
    # =======================================================================

    def power(
        self,
        state: bool
    ) -> None:
        """
        turn the power on (True) or off (False)
        """
        
        self._power.write( state )       

    # =======================================================================


# ===========================================================================

class lcd_spi_cd:
    """
    lcd interface for spi and command/data
    
    :param spi: ($$ref( "gf.spi" ) )
        spi interface (miso not used)
        
    :param data_command: ( int | str | $$ref( "can_pin_out" ) )
        data / command pin, high for data, low for command
        
    :param chip_select: ( int | str | $$ref( "can_pin_out" ) )
        chip select pin, active low
    
    This class provides the basic command & data interface
    for a spi LCD with a command / data pin.
    """

    # =======================================================================    

    def __init__(
        self,
        spi: "gf.spi", 
        data_command: int | str | gf.can_pin_out,
        chip_select: int | str | gf.can_pin_out,
    ) -> None:
        self._spi = spi
        self._data_command = gf.pin_out( data_command )
        self._chip_select = gf.pin_out( chip_select )

    # =======================================================================    

    def write_command(
        self, 
        command: [ int, [ int ] ] = None, 
        data = None,
        buffer = None
    ) -> None:
        """
        write command and/or data
        
        :param command: (None, int)
            a command byte to be send to the lcd
        
        :param data: (None, sequence of bytes)
            data bytes to be send to the lcd
        
        This method writes a command (integer, optional)
        and data (also optional) to the lcd.
        The data must be acceptabel for a bytes() call.
        """
        
        self._chip_select.write( 0 )

        if command is not None: 
            self._data_command.write( 0 )
            #print( command )
            if isinstance( command, int ):
                command = [ command ]
            #print( comand )    
            self._spi.write( bytearray( command ) )
            #self._chip_select.write( 1 )
        
        if data is not None:
            self._data_command.write( 1 )
            #self._chip_select.write( 0 )
            self._spi.write( bytes( data ) )
            
        if buffer is not None:
            self._data_command.write( 1 )
            #self._chip_select.write( 0 )
            self._spi.write( buffer )
            
        self._chip_select.write( 1 )    

    # =======================================================================    


# ===========================================================================    

def _encode_565( a: int, b: int, c: int ) -> int:
    v = ( ( a >> 3 ) << 11 ) | ( ( b >> 2 ) << 5 ) | ( c >> 3 )
    return ( ( v & 0xFF ) << 8  ) | ( ( v >> 8 ) & 0xFF )    


# ===========================================================================

class generic_color_lcd(
    gf.canvas,
    lcd_spi_cd,
    lcd_reset_backlight_power
):
    """
    generic lcd driver for SPI color lcds
           
    :param size: :class:`~godafoss.xy`
        size of the display area in pixels in x and y direction

    :param spi: machine.SPI
        SPI channel that connects to the driver chip

    :param data_command
        data / command pin to the driver chip

    :param chip_select
        SPI chip select pin to the driver chip (active low)

    :param reset
        reset pin to the driver chip (optional, active low)
        
        The constructor resets the driver chip.
        The lcd_reset_backlight_power:reset() method can be used
        to reset the chip.        

    :param backlight
        backlight pin to the driver chip (optional, active high)
        
        The constructor enables the backlight.
        The lcd_reset_backlight_power:backlight() method can be used
        to switch the power.        

    :param power
        power enable pin to the driver chip (optional, active high)
        
        The constructor enables power to the driver chip.
        The lcd_reset_backlight_power:power() method can be used
        to switch the power on or off.

    :param background: :class:`~godafoss.color`
        default background color (default: colors.black)
        
        This is the default for the clear() method.
        The inverse of the background is the default for writing
        a monochrome shape.
        
    :param offset: :class:`~godafoss.xy`
        offset of the displayed area
    
        LCD modules can have an margin of hidden pixels 
        to the left and top of the displayed area.
        This parameter is the offset of the first displayed pixel
        (default: xy(0,0)).           

    :param invert: bool
        invert the luminosity of colors (default: False)

    :param mirror_x: bool
        mirror (reverse) the x adressing (default: False)

    :param mirror_y: bool
        mirror (reverse) the y adressing (default: False)

    :param swap_xy: bool
        swap the x and y addressing (default: False)

    :param color_order: str | None
        color order
    
        This parameter specifies order in which the colors must be stored
        in the chip to be displayed correctly on the LCD.
        The default is RGB, which is correct for most chips.
        For instancem, for a chip that swap the red and blue channels
        specify "BGR".

        In color mode, this driver uses a RAM canvas of 2 bytes per pixel, 
        which can be more than your target has available.
        In monochrome mode (color_order = None) it uses a RAM canvas 
        of 8 pixels per byte, but a downside is that flushing takes
        longer because data for the SPI transactions must
        be constructed on the fly.
        
    :param mechanisms: int
        the mechanism used for monochrome data transport
        
        This parameter selects the mechanism used by the flush
        method to transport data to the LCD when the LCD is
        use in monochrome mode.
        
        The default value of 0 uses a 4k lookup table.
        When this memory use is a problem, 1 can be specified.
        This setting uses a line buffer of 2 bytes per pixel in the x
        direction (256 bytes for 128 x 128 display) and calculates
        the data on the fly, which is much slower.
        
        For a RP2040 chip setting 2 uses a PIO engine to
        generate the data.
        This is fast and requires no buffer, but uses a PIO engine,
        and can only display the colors black and white.
        
        +------------------------------------------------------+
        | Raspberry Pi Pico RP2040 ST7735 color LCD 128 x 128  |
        +-----------------+--------------+---------------------+
        | use             | method       | flush takes         |
        +-----------------+--------------+---------------------+
        | color           | n.a.         | 80 ms               |
        +-----------------+--------------+---------------------+
        | monochrome      | 0            | 114 ms              |
        +-----------------+--------------+---------------------+
        | monochrome      | 1            | 374 ms              |
        +-----------------+--------------+---------------------+
        | monochrome      | 2            | 114 ms              |
        +-----------------+--------------+---------------------+       
    
    This class is the base for various SPI color LCDs.
    """

    # =======================================================================
    
    class commands:
        nop        = gf.gf.const( 0x00 )
        swreset    = gf.gf.const( 0x01 )
        slpin      = gf.gf.const( 0x10 )
        slpout     = gf.gf.const( 0x11 )
        invoff     = gf.gf.const( 0x20 )
        invon      = gf.gf.const( 0x21 )        
        dispoff    = gf.gf.const( 0x28 )
        dispon     = gf.gf.const( 0x29 )
        caset      = gf.gf.const( 0x2A )
        raset      = gf.gf.const( 0x2B )
        ramwr      = gf.gf.const( 0x2C )        
        madctl     = gf.gf.const( 0x36 )
        colmod     = gf.gf.const( 0x3A )   
        
    # =======================================================================

    def __init__( 
        self, 
        size: gf.xy, 
        spi: "machine.SPI", 
        data_command: [ int, gf.can_pin_out ],
        chip_select: [ int, gf.can_pin_out ] = None, 
        reset: [ int, gf.can_pin_out ] = None,
        backlight: [ int, gf.can_pin_out ] = None,
        power: [ int, gf.can_pin_out ] = None,
        background: gf.color = gf.colors.black, 
        monochrome: bool = False,
        color_order: str = "RGB",
        mechanism: int = 0,
        invert: bool = False,
        mirror_x: bool = False,
        mirror_y: bool = False,
        swap_xy: bool = False,
        offset = gf.xy( 0, 0 ),
        x_deadband = 0,
        orientation: gf.orientation = gf.orientation.north
    ):
        
        if not isinstance( offset, gf.xy ):
            offset = offset[ orientation - gf.orientation.north ]
        
        if orientation == gf.orientation.north:
            pass
        
        elif orientation == gf.orientation.east:
            size = gf.xy( size.y, size.x )
            offset = gf.xy( offset.y, offset.x )
            swap_xy = not swap_xy
            mirror_y = not mirror_y
            
        elif orientation == gf.orientation.south:
            mirror_x = not mirror_x
            mirror_y = not mirror_y
            
        elif orientation == gf.orientation.west:
            size = gf.xy( size.y, size.x )
            offset = gf.xy( offset.y, offset.x )
            swap_xy = not swap_xy
            mirror_x = not mirror_x
              
        else:
            raise Exception( f"invalid orientation {orientation}" )        
        
        self._color_order = color_order
        self._invert = invert
        self._mirror_x = mirror_x
        self._mirror_y = mirror_y
        self._swap_xy = swap_xy
        self._offset = offset
        
        gf.canvas.__init__(
            self,
            size = size,
            is_color = not monochrome,
            background = background
        )

        gf.lcd_reset_backlight_power.__init__( 
            self, 
            reset = gf.pin_out( reset ).inverted(), 
            backlight = backlight, 
            power = power,
            
            # longest required reset:
            #     10 us low,
            #     120 ms wait for reset to effectuate
            # (ST7735 datasheet 9.16)
            reset_duration = 10,
            reset_wait = 120_000
        )
        
        gf.lcd_spi_cd.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
        
        # software reset    
        #self.write_command( self.commands.swreset )
        #gf.sleep_us( 5_000 )   
        
        # color mode 16-bit RGB 565
        self.write_command( self.commands.colmod, [ 0x55 ] ) 
        
        # swapping and mirroring
        m = 0x00
        if self._swap_xy:
            m |= 0x20
        if self._mirror_x:
            m |= 0x40
        if self._mirror_y:
            m |= 0x80
        self.write_command( self.commands.madctl, [ m ] )  

        # row and column length
        self.write_command( self.commands.caset, [
            0, 0, self.size.x >> 8, self.size.x & 0xFF ])
        self.write_command( self.commands.raset, [
            0, 0, self.size.y >> 8, self.size.y & 0xFF ])   
            
        # inverted or normal    
        self.write_command(
            self.commands.invon 
                if self._invert else 
            self.commands.invoff 
        )            
          
        # leave sleep mode
        self.write_command( self.commands.slpout )
        gf.sleep_us( 120_000 )  

        # display on
        self.write_command( self.commands.dispon )        
               
        if self.is_color:
        
            color_order = color_order.upper()
            if color_order == "RGB":
                self._encode = lambda c: _encode_565( c.red, c.green, c.blue )
                
            elif color_order == "RBG":
                self._encode = lambda c: _encode_565( c.red, c.blue, c.green )
                
            elif color_order == "GRB":
                self._encode = lambda c: _encode_565( c.green, c.red, c.blue )
                
            elif color_order == "GBR":
                self._encode = lambda c: _encode_565( c.green, c.blue, c.red )
                 
            elif color_order == "BRG":
                self._encode = lambda c: _encode_565( c.blue, c.red, c.green )
                
            elif color_order == "BGR":
                self._encode = lambda c: _encode_565( c.blue, c.green, c.red )
                
            else:
                raise ValueError( "unsupported color order '%s'" % color_order )   
        
            # import gc; gc.collect()
            self._buffer = bytearray( 
                2 * self.size.y * ( self.size.x + x_deadband ) )
            self._framebuffer = framebuf.FrameBuffer(
                self._buffer, 
                self.size.x + x_deadband, 
                self.size.y, 
                framebuf.RGB565 
            )
            
            self._flush_data_transport = \
               self._flush_data_transport_color                        
            
        else:    
            self._encode = lambda x: x
        
            self._buffer_size = \
                ( ( self.size.x + x_deadband ) * ( self.size.y ) + 7 ) // 8
            self._buffer = bytearray( self._buffer_size )
            self._framebuffer = framebuf.FrameBuffer(
                self._buffer, 
                self.size.x + x_deadband, 
                self.size.y, 
                framebuf.MONO_HLSB 
            )
            
            if mechanism == 0:
                
               # create fast-lookup for 8 pixels at a time
               # (uses 4k RAM)
               self._pixels = [ bytearray( 16 ) for _ in range( 256 ) ]
               for v in range( 256 ):
                    i = 0
                    m = 0x80
                    for _ in range( 8 ):
                        c = 0xFF if v & m != 0 else 0x00
                        self._pixels[ v ][ i ] = c                  
                        self._pixels[ v ][ i + 1 ] = c
                        m = m >> 1
                        i += 2
                        
               self._flush_data_transport = \
                   self._flush_data_transport_monochrome_lookup                        
                
            elif mechanism == 1:
                
               self._line_buffer = bytearray( 2 * self.size.x )
               self._flush_data_transport = \
                  self._flush_data_transport_monochrome_line_buffer                        
                
            elif mechanism == 2:
                
                # each GPIO pin has 2 registers, starting at 0x40014000
                # a register is 4 bytes, control is the 2nd register                
                io_addresses = (
                    0x40014000 + self._spi.sck * 8 + 4,
                    0x40014000 + self._spi.mosi * 8 + 4
                )
                self.spi_gpio = remember( io_addresses )
                self.make_fsm()                  
                self.spi_pio = remember( io_addresses )
                self.spi_gpio.restore()
        
                self._flush_data_transport = \
                    self._flush_data_transport_monochrome_rp2_pio
        
            else:
                raise ValueError( "undefined mechanism '%d'" % mechanism )
            
    # =======================================================================
       
    def _flush_implementation(
        self,
        forced: bool
    ) -> None:     
        
        x_end = self.size.x - 1 + self._offset.x
        self.write_command( self.commands.caset, [
            0x00, self._offset.x, 
            x_end // 256, x_end % 256
        ])
        
        y_end = self.size.y - 1 + self._offset.y
        self.write_command( self.commands.raset, [ 
            0x00, self._offset.y,
            y_end // 256, y_end % 256
        ])
        
        self._flush_data_transport()             
                
    # =======================================================================
    
    def _flush_data_transport_color( self ):
        self.write_command( self.commands.ramwr, buffer = self._buffer )
      
    # =======================================================================
    
    #@micropython.native      
    def _flush_data_transport_monochrome_lookup( self ):       
        self.write_command( self.commands.ramwr )
        self._data_command.write( 1 )
        self._chip_select.write( 0 )
        
        _n = gf.const( 8 )
        _m = gf.const( _n * 16 )
        p = bytearray( _m )
        i = 0
        
        # optimization by avoiding lookup, ~ 10% faster
        pp = self._pixels
        ww = self._spi.write
        
        for b in self._buffer: 
            p[ i : i + 16 ] = pp[ b ]
            i += 16
            if i >= _m:
                ww( p )
                i = 0
                
        self._chip_select.write( 1 )        
      
    # =======================================================================
    
    #@micropython.native      
    def _flush_data_transport_monochrome_line_buffer( self ):       
        self.write_command( self._driver.command.ramwr )
        self._data_command.write( 1 )
        self._chip_select.write( 0 )
        for y in range( self.size.y ):
            for x in range( self.size.x ):
                c = 0xFF if self._framebuffer.pixel( x, y ) else 0x00
                self._line_buffer[ 2 * x ] = c                  
                self._line_buffer[ 2 * x + 1 ] = c                  
            self._spi.write( self._line_buffer )         
        self._chip_select.write( 0 )
     
    # =======================================================================

    def _clear_implementation( 
        self,
        ink: gf.color
    ):
        self._framebuffer.fill( self._encode( ink ) )
        
    # =======================================================================
        
    def _write_pixel_implementation( 
        self, 
        location: ( int, gf.xy ), 
        ink: gf.color
    ):
        self._framebuffer.pixel(
            location.x,
            location.y,
            self._encode( ink )
        )
        
    # =======================================================================
    
    
# ===========================================================================

class pcd8544( 
    gf.canvas, 
    lcd_reset_backlight_power, 
    lcd_spi_cd 
):
    """
    pcd8544 SPI b/w lcd controller driver
    
    $macro_insert lcd_reset_backlight_power_functionality    
    
    :param size: :class:`~godafoss.xy`
        horizontal and vertical size, in pixels
        
    :param spi: machine.SPI
        spi bus (miso not used)
        
    :param data_command: $macro_insert make_pin_out_types
        dc (data/command) pin of the chip
        
    :param cs: $macro_insert make_pin_out_types
        cs (chip select) pin of the chip
        
    $macro_insert lcd_reset_backlight_power_parameters
        
    :param background: bool
        background 'color', default (False) is off (white-ish)
    
    This is a driver for a pcd8544 black & white lcd controller.
    This chip was used with an 84 x 48 lcd in the once-popular 
    Nokia model 5110  telephone, 
    hence it is often called a (Nokia) 5110 lcd.
    This type of lcd is cheap and available from lots of sources,
    but the quality is often low (dead-on-arrival), 
    and the pinout varies.
    
    $insert_image( "pcf8544", 1, 200 )
    
    The pcb module shown has a backlight pin that must be connected
    to the (3.3V) power via a suitable resistor (330 Ohm is OK).
    
    $macro_insert lcd_reset_backlight_power_functionality
    
    $macro_insert canvas_monochrome
    """
    
    # =======================================================================    

    class _commands:   
        """chip commands"""
    
        # common
        FUNCTION_SET     = gf.const( 0x20 ) # 0 basic, 1 extended
        
        # basic
        DISPLAY_CONTROL  = gf.const( 0x08 )
        BANK_ADDR        = gf.const( 0x40 ) # y pos, by 8 rows (0~5 )    
        COL_ADDR         = gf.const( 0x80 ) # x pos (0~83 )
        
        # extended
        TEMP_CONTROL     = gf.const( 0x04 )
        SET_BIAS         = gf.const( 0x10 )
        SET_VOP          = gf.const( 0x80 )
    
    # =======================================================================    

    def __init__( 
        self, 
        size: gf.xy, 
        spi: "machine.SPI", 
        data_command: [ int, gf.can_pin_out ],
        chip_select: [ int, gf.can_pin_out ],
        reset: [ None, int, gf.can_pin_out ] = None, 
        backlight: [ None, int, gf.can_pin_out ] = None, 
        power: [ None, int, gf.can_pin_out ] = None,
        background: bool = False
    ) -> None:
        gf.canvas.__init__( 
            self, 
            size = size,
            is_color = False,
            background = background
        )
        gf.lcd_reset_backlight_power.__init__( 
            self, 
            reset = gf.make_pin_out( reset ).inverted(), 
            backlight = backlight, 
            power = power
        ) 
        gf.lcd_spi_cd.__init__( 
            self, 
            spi = spi, 
            data_command = data_command, 
            chip_select = chip_select
        ) 

        self._buffer = bytearray(( self.size.y // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB 
        )    
        
        # inlitialize the chip
        
        # select exteded instruction set
        self.write_command( self._commands.FUNCTION_SET    | 0x01 )  
        
        # Vop = 110000
        self.write_command( self._commands.SET_VOP         | 0x48 ) 

        # TCx = 10
        self.write_command( self._commands.TEMP_CONTROL    | 0x02 )  
        
        # BSx = 011
        self.write_command( self._commands.SET_BIAS        | 0x03 )  
        
        # select basic instruction set
        self.write_command( self._commands.FUNCTION_SET    | 0x00 )  
        
        # normal mode = 100
        self.write_command( self._commands.DISPLAY_CONTROL | 0x04 )  
        
    # =======================================================================    

    def _write_pixel_implementation( 
        self, 
        location: gf.xy, 
        ink: bool
    ) -> None:
        """
        write to a single pixel
        """
               
        self._framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )
        
    # =======================================================================    

    def _flush_implementation( self, forced ) -> None:
        """
        flush the framebuffer to the display
        """
        
        # set write pointer(s); write pixel data
        self.write_command( self._commands.COL_ADDR  | 0 )
        self.write_command( self._commands.BANK_ADDR | 0, self._buffer )

    # =======================================================================    

    def _clear_implementation( 
        self, 
        ink: bool
    ) -> None:
        """
        clear the framebufer
        """

        self._framebuf.fill( 0xFF if ink else 0x00 )      
        
    # =======================================================================
         
         
# ===========================================================================

class ks0107( 
    gf.canvas, 
    lcd_reset_backlight_power, 
):
    """
    dual ks0107 b/w lcd controller driver
    
    reset has yet to be rewritten
    
    $macro_insert lcd_reset_backlight_power_functionality    
    
    :param size: :class:`~godafoss.xy`
        horizontal and vertical size, in pixels
        
    :param spi: machine.SPI
        spi bus (miso not used)
        
    :param data_command: $macro_insert make_pin_out_types
        dc (data/command) pin of the chip
        
    :param cs: $macro_insert make_pin_out_types
        cs (chip select) pin of the chip
        
    $macro_insert lcd_reset_backlight_power_parameters
        
    :param background: bool
        background 'color', default (False) is off (white-ish)
    
    This is a driver for a 128 x 64 dual KS0107 black & white lcd.
    The ones I know are for 5V, but the output from the MicroPython
    chip to the LCD display can be 3.3V.
    
    $insert_image( "ks0107", 1, 200 )
    
    $macro_insert lcd_reset_backlight_power_functionality
    
    $macro_insert canvas_monochrome
    """
        
    # =======================================================================    

    def __init__( 
        self, 
        data: [ gf.port_out ],
        cs1: [ int, gf.can_pin_out ],
        cs2: [ int, gf.can_pin_out ],
        cd: [ int, gf.can_pin_out ],
        enable: [ int, gf.can_pin_out ],
        wr: [ int, gf.can_pin_out ] = None,
        reset: [ None, int, gf.can_pin_out ] = None, 
        backlight: [ None, int, gf.can_pin_out ] = None, 
        power: [ None, int, gf.can_pin_out ] = None,
        background: bool = False
    ) -> None:
        
        self.data = gf.make_port_out( data )
        self.cs1 = gf.pin_out( cs1 )
        self.cs2 = gf.pin_out( cs2 )
        self.cd = gf.pin_out( cd )
        self.enable = gf.pin_out( enable )
        self.enable.write( 1 )
        self.wr = gf.pin_out( wr )
        self.wr.write( 0 )
        
        gf.canvas.__init__( 
            self, 
            size = gf.xy( 128, 64 ),
            is_color = False,
            background = background
        )
        gf.lcd_reset_backlight_power.__init__( 
            self, 
            reset = gf.pin_out( reset ).inverted(), 
            backlight = backlight, 
            power = power
        )
        
        self._buffer = bytearray(( self.size.y // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB 
        )    
          
        # display on
        self.write_command( 0x3f )
        
        # set start address
        self.write_command( 0xc0 )
        
        
    # =======================================================================
    
    def write_command( self, command ):
        """
        write the commadn to both chips
        """
        self.cd.write( 0 )
        self.cs1.write( 0 )
        self.cs2.write( 0 )
        self.data.write( command )
        self.enable.write( 1 )  
        self.enable.write( 0 )  

    # =======================================================================    

    def _write_pixel_implementation( 
        self, 
        location: gf.xy, 
        ink: bool
    ) -> None:
        """
        write to a single pixel
        """
               
        self._framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )
        
    # =======================================================================    

    def _flush_implementation( self, forced ) -> None:
        """
        flush the framebuffer to the display
        """          
        
        for n, data in enumerate( self._buffer ):
            
            if ( n % 64 ) == 0:                
                
                self.write_command( 0x40 )
                self.write_command( 0xb8 | ( n // 128 ) )             
                
                first = ( n % 128 ) > 63
                self.cs1.write( first ) # not only here (or both!) makes 2 receive the same
                self.cs2.write( not first )   # not or plain doesn't matter, even 1 is OK (not connected??)         
            
                self.cd.write( 1 )
                
            self.data.write( data )
            self.enable.write( 1 )  
            self.enable.write( 0 )             

        
   # =======================================================================    

    def _clear_implementation( 
        self, 
        ink: bool
    ) -> None:
        """
        clear the framebufer
        """

        self._framebuf.fill( 0xFF if ink else 0x00 )      
        
    # =======================================================================
         

# ===========================================================================

class hd44780( gf.terminal ):
    """
    hd44780 character LCD interface
    
    This class implements an interface to an hd44780 character LCD.
    
    $$insert_image( "hd44780-picture", 300 )
    
    The hd44780 is the standard chip for interfacing small dot-character
    LCD interfaces.
    It can display the ASCII table characters, 8 characters (0..7)
    that can be user-defined as 5x7 pixels, and a an upper 128 characters
    (128...255) that vary with the chip variant, often Japanese characters.
    
    The chip and its digital pins run at 5V.
    The contrast input can in most cases be connected to 0V (ground), but
    better use a 10k potentiometer between 0V and 5V. Some
    displays (mostly extended-temperature-range types) need the lower
    size of this potentiometer tied to a negative voltage, for instance -5V.
    
    The digital interface to the chip has 8 data lines, but the chip can be
    configured to use only 4. This adds some complexity to the driver
    software and slows it down a little, but the saving of 4 micro-controller
    more than compensates for this, hence nearly all software
    (including this driver) for is for the 4-bit interface.
    Note for the 4-bit interface the 4 highest data pins (D4..D7) are used.
    The lower 4 can be left unconnected.
    
    The chip has some locations that can be writen and also read back,
    but this offers little advantage, so most software (including this driver)
    only writes to the chip, thus saving another pin.
    Hence 6 digital pins (+ ground and 5V)
    are needed to interface to an hd44780 display:
    4 data lines, the R/S line (selects between command and data),
    and the E line (a strobe for the command).
    
    $-$insert_image( "hd44780-connection", 300 )
    
    (Some larger displays use not one but two hd44780 chips.
    This driver is not compatible with such LCDs.)
    
    Most hd44780 LCDs have a single row of connections,
    with the following pinout:
    
    $-$insert_image( "hd44780-pinout", 300 )
    
    But as always, check the datasheet (in this case of the LCD) to be sure!
    
    The hd44780 implements the ostream interface, but it doesn't scroll:
    while the cursor is outside the visible characters 
    (beyond the end of the line,
    or beyond the number of lines) any character writes will be ignored.
    Some characters are treated special:
    
        - '\\n' clears the rest of the line, and then
          moves to the first position of the next line
        - '\\r' puts the cursor at the start of the current line
        - '\\v' moves the cursor to the top-left position
    
    The best way to get a flicker-free display is to overwite
    instead of clear-and-then-write:
    use '\\c' to got to the 'origin', then rewrite the whole display,
    using '\\n' to go to a next line 
    (because it clears the remainder of the line).
    """

    # =======================================================================    

    def __init__( 
        self,
        *,
        size, 
        data: [ gf.port_out, gf.port_in_out, gf.port_oc ],
        rs : [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ], 
        e: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ], 
        rw: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None, 
        backlight: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None
    ):
        gf.terminal.__init__( self, size )

        self._data = data.as_port_out()
        self._rs = gf.pin_out( rs )
        self._e = gf.pin_out( e )
        self._rw = gf.pin_out( rw )
        self.backlight = gf.pin_out( backlight )
        self._init()

    # =======================================================================    

    def _init( self ):
        """initialize the hd44780 chip to 4-bit mode"""
        self._rw.write( 0 )
        self.backlight.write( 1 )

        # give LCD time to wake up
        self._e.write( 0 )
        self._rs.write( 0 )
        gf.sleep_us( 100_000  )

        # interface initialization: make sure the LCD is in 4 bit mode
        # (magical sequence, taken from the HD44780 data-sheet)
        self._write4( 0x03 )
        gf.sleep_us( 15_000 )
        self._write4( 0x03 )
        gf.sleep_us( 100 )
        self._write4( 0x03 )
        self._write4( 0x02 )            # 4 bit mode

        # functional initialization
        self.command( 0x28 )            # 4 bit mode, 2 lines, 5x8 font
        self.command( 0x0C )            # display on, no cursor, no blink
        self.clear()                    # clear display, 'cursor' home
        self.cursor_set( gf.xy( 0, 0 ) )   # 'cursor' home

    # =======================================================================    

    def _write4( self, data: int ) -> None:
        gf.sleep_us( 10 )
        self._data.write( data )
        gf.sleep_us( 20 )
        self._e.write( 1 )
        gf.sleep_us( 20 )
        self._e.write( 0 )
        gf.sleep_us( 100 )

    # =======================================================================    

    def data( self, data: int ) -> None:
        """write a data byte to the hd44780"""
        self._rs.write( 1 )
        self._write4( data >> 4 )
        self._write4( data )

    # =======================================================================    

    def command( self, data: int ) -> None:
        """write a command to the hd44780"""
        self._rs.write( 0 )
        self._write4( data >> 4 )
        self._write4( data )

    # =======================================================================    

    def clear( self ) -> None:
        """clear the display and put the cursor at xy( 0, 0 ) """
        self.command( 0x01 )
        gf.sleep_us( 5_000 )
        self.cursor_set( gf.xy( 0, 0 ) )

    # =======================================================================    

    def _cursor_set_implementation( self ) -> None:
        # the NVI cursor_set() method has already set the cursor 

        if self.size.y == 1:
            if self.cursor.x < 8:
                self.command( 0x80 + self.cursor.x )
            else:
                self.command( 0x80 + 0x40 + ( self.cursor.x - 8 ) )
        else:
            if self.size.y == 2:
                self.command(
                    0x80
                    + ( 0x40 if self.cursor.y > 0 else 0x00 )
                    + self.cursor.x
                )
            else:
                self.command(
                    0x80
                     + ( 0x40 if ( self.cursor.y & 0x01 ) != 0 else 0x00 )
                     + ( 0x14 if ( self.cursor.y & 0x02 ) != 0 else 0x00 )
                     + self.cursor.x
                )

    # =======================================================================    

    def _write_implementation( self, c: chr ) -> None:

        # the NVI write() method handles the cursor update

        # handle the gap for 1-line displays
        if ( self.size.y == 1 ) and ( self.cursor.x == 8 ):
            self.cursor_set( self.cursor )

        self.data( ord( c ) )
        
    # =======================================================================    

    def demo( self ) -> None:
        print( "hd44780 demo: blink Hello world!" )
        self.clear()
        self.write( "Hello world!\n2\n3\n4" )


# ===========================================================================

def hd44780_pcf8574a( 
    size: gf.xy, 
    bus, 
    address = 0
) -> hd44780:
    chip = gf.pcf8574a( bus, address )
    data = gf.make_port_in_out( chip.p4, chip.p5, chip.p6, chip.p7 )
    rs = chip.p0
    e = chip.p2
    rw = chip.p1
    backlight = chip.p3
    return hd44780( size, data, rs, e, rw, backlight )    
     

# ===========================================================================

def hd44780_pcf8574( 
    size: gf.xy, 
    bus, 
    address = 7
) -> hd44780:
    chip = gf.pcf8574( bus, address )
    data = gf.make_port_in_out( chip.p4, chip.p5, chip.p6, chip.p7 )
    rs = chip.p0
    e = chip.p2
    rw = chip.p1
    backlight = chip.p3
    return hd44780( size, data, rs, e, rw, backlight )    
     
     
# =========================================================================== 