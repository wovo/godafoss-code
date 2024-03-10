# ===========================================================================
#
# file     : gf_tm1640.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class tm1640( gf.tm16xx, gf.canvas ):
    """
    tm1640 LED matrix display interface driver
    
    This class controls a tm1640 LED matrix display interface chip.
    The mandatory constructor parameters are the size of the
    display, and the interface pins sclk and dio.
    The optional parameters are the background (default is False == disabled)
    and the bightness (0..7, default is 0)
    
    The driver is buffered: a clear() call is required to update
    the display.
    
    The tm1637 hardware interface is i2c-like, but it is not
    meant for multiple chips as it does not use
    a slave address byte or ack bits.
    The driver uses output pins for  the sclk and din pins,
    hence no pull-up resistors are needed.
    """

    # =======================================================================

    def __init__( 
        self, 
        size: gf.xy,
        sclk: [ int, pin_out, pin_in_out, pin_oc ], 
        din: [ int, pin_out, pin_in_out, pin_oc ], 
        background: bool = False,
        brightness: int = 0
    ) -> None:

        self._sclk = gf.make_pin_out( sclk )
        self._din = gf.make_pin_out( din )
        self._sclk.write( 1 )
        self._din.write( 1 ) 
        gf.sleep_us( 1 )
        
        gf.canvas.__init__(
            self,
            size = size,
            is_color = False,
            background = background
        )
        
        tm16xx.__init__(
            self,
            size = size,
            brightness = brightness
        )
       
    # =======================================================================

    def _write_pixel_implementation( 
        self, 
        location: gf.xy, 
        ink: bool
    ) -> None:       
        self._framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )
            
    # =======================================================================    

    def _clear_implementation(
        self,
        ink : bool
    ) -> None:
        self._framebuf.fill( 0xFF if ink else 0x00 )             
            
    # =======================================================================
            
            
    def _start( self ) -> None:
        self._din.write( 0 )
        gf.sleep_us( 1 )
        self._sclk.write( 0 )
        gf.sleep_us( 1 )

        
    # =======================================================================

    def _stop( self ) -> None:
        self._din.write( 0 )
        gf.sleep_us( 1 )
        self._sclk.write( 1 )
        gf.sleep_us( 1 )
        self._din.write( 1 )
        gf.sleep_us( 1 )
        
    # =======================================================================
        
    def _write_byte(
        self,
        b: int
    ) -> None:
        # write 8 bits, LSB first
        for _ in range( 8 ):
            self._din.write( ( b & 0x01 ) != 0 )
            b = b >> 1
            gf.sleep_us( 1 )
            self._sclk.write( 1 )
            gf.sleep_us( 1 )
            self._sclk.write( 0 )
            gf.sleep_us( 1 )
            
    # =======================================================================

        
# ===========================================================================
