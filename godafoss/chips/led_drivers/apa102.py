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
   
class apa102( gf.neopixels ):
    """
    """

    def __init__( 
        self, 
        ci: int,
        di: int,
        n: int, 
        background = gf.colors.black, 
        order: str = "RGB"
    ):
        self.ci = gf.make_pin_out( ci )
        self.di = gf.make_pin_out( di )
        
        self._pixels = []
        for _ in range( n ):
            self._pixels.append( ( 0, 0, 0 ) )
            
        gf.neopixels.__init__( self, n, background, order )

    # =======================================================================
    
    def _write_byte( self, byte ):
        for _ in range(8):
            self.di.write ( byte & 0x80 )
            self.ci.write( 1 )
            byte <<= 1
            self.ci.write( 0 )

    # =======================================================================
    
    def _flush_implementation(
        self,
        forced = True
    ):
        for _ in range( 4 ):
            self._write_byte( 0 )

        for pixel in self._pixels:
            self._write_byte( 0xFF )
            for byte in pixel:
                self._write_byte( byte )

        for _ in range( 4 ):
            self._write_byte( 0xFF )

    # =======================================================================
    
# ===========================================================================
