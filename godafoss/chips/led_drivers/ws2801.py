# $$document( 0 )

# ===========================================================================
#
# file     : gf_ws2801.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class ws2801( gf.neopixels ):
    """
    driver for neopixels with separate clock (ck) and data (si) lines
    """

    # =======================================================================

    def __init__( 
        self, 
        clock: [ int, pin_out, pin_in_out, pin_oc ],
        data: [ int, pin_out, pin_in_out, pin_oc ],
        n: int, 
        background = colors.black, 
        order: str = "RGB"
    ):
        self._clock = make_pin_out( clock )
        self._data = make_pin_out( data )
        self._n = n
        self._background = background
        self._pixels = [ self._background for _ in range( self._n ) ]
        gf.neopixels.__init__( 
            self, 
            n, 
            self._background,
            order
        )

    # =======================================================================
    
    def _write_byte( self, b ):
        for _ in range( 8 ):
            self._data.write( ( b & 0x80 ) != 0 )
            b = b << 1
            sleep_us( 1 )
            
            self._clock.write( 1 )
            sleep_us( 1 )
            
            self._clock.write( 0 )
            sleep_us( 1 )

    # =======================================================================

    def flush( self ): 
        self._clock.write( 0 )
        sleep_us( 500 )
        for p in self._pixels:
            self._write_byte( p.red )
            self._write_byte( p.blue )
            self._write_byte( p.green )
            

# ===========================================================================
