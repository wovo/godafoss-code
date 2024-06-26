# ===========================================================================
#
# file     : ks0107.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import framebuf

import godafoss as gf


# ===========================================================================

class ks0107( 
    gf.canvas, 
    gf.lcd_reset_backlight_power, 
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
        cs1: [ int, pin_out, pin_in_out, pin_oc ],
        cs2: [ int, pin_out, pin_in_out, pin_oc ],
        cd: [ int, pin_out, pin_in_out, pin_oc ],
        enable: [ int, pin_out, pin_in_out, pin_oc ],
        wr: [ int, pin_out, pin_in_out, pin_oc ] = None,
        reset: [ None, int, pin_out, pin_in_out, pin_oc ] = None, 
        backlight: [ None, int, pin_out, pin_in_out, pin_oc ] = None, 
        power: [ None, int, pin_out, pin_in_out, pin_oc ] = None,
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
