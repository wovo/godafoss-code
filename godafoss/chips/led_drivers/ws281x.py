# ===========================================================================
#
# file     : gf_apa102.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

#$$document( 0 )


# ===========================================================================

class ws281x( gf.neopixels ):
    """
    requires neopixel support in the target, Teensy 4.1 by default doesn't
    """

    def __init__( 
        self, 
        d: int,
        n: int, 
        background = gf.colors.black, 
        order: str = "RGB"
    ):
        import machine, neopixel
        self._pixels = neopixel.NeoPixel( machine.Pin( d ), n )
        
        for i in range( n ):
            self._pixels[ i ] = ( 0, 0, 0 )
            
        gf.neopixels.__init__( self, n, background, order )

    # =======================================================================
    
    def _flush_implementation(
        self,
        forced = True
    ):
        self._pixels.write()
        
    # =======================================================================
    
# ===========================================================================
