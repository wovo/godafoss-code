# ===========================================================================
#
# file     : generic_color_lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from micropython import const
import framebuf
import machine

import godafoss as gf

    
# ===========================================================================

def _encode_565( a: int, b: int, c: int ) -> int:
    v = ( ( a >> 3 ) << 11 ) | ( ( b >> 2 ) << 5 ) | ( c >> 3 )
    return ( ( v & 0xFF ) << 8  ) | ( ( v >> 8 ) & 0xFF )    

# ===========================================================================

class generic_color_lcd(
    gf.canvas,
    gf.lcd_spi_cd,
    gf.lcd_reset_backlight_power
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
        nop        = gf.const( 0x00 )
        swreset    = gf.const( 0x01 )
        slpin      = gf.const( 0x10 )
        slpout     = gf.const( 0x11 )
        invoff     = gf.const( 0x20 )
        invon      = gf.const( 0x21 )        
        dispoff    = gf.const( 0x28 )
        dispon     = gf.const( 0x29 )
        caset      = gf.const( 0x2A )
        raset      = gf.const( 0x2B )
        ramwr      = gf.const( 0x2C )        
        madctl     = gf.const( 0x36 )
        colmod     = gf.const( 0x3A )   
        
    # =======================================================================

    def __init__( 
        self, 
        size: xy, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: [ int, pin_out, pin_in_out, pin_oc ] = None,
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
        
        _n = const( 8 )
        _m = const( _n * 16 )
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
        ink: color
    ):
        self._framebuffer.fill( self._encode( ink ) )
        
    # =======================================================================
        
    def _write_pixel_implementation( 
        self, 
        location: ( int, xy ), 
        ink: color
    ):
        self._framebuffer.pixel(
            location.x,
            location.y,
            self._encode( ink )
        )
        
    # =======================================================================
    
# ===========================================================================
