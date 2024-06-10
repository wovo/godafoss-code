# ===========================================================================
#
# file     : gf__edge_rp2.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class _edge_rp2( gf._edge ):
    
    def __init__( self ):
        
        v = gf.gpio_adc( 28 ).read().scaled( 0, 65535 )
    
        # 10k, 10k
        if gf.within( v, 31000, 35000 ):

            self.system = "original RP2040 rp2 or rp2w"
            self.pins = ( 18, 19, 16, 17, 26, 27, 13 , 12 )

        
        # 10k, 15k        
        elif gf.within( v, 24000, 28000 ): 

            self.system = "01Space RP2040-0.42 OLED"
            self.pins = ( 20, 24, 25, 26, 5, 6, 4, 3 )

        else:
            print( "rp2 unrecognized adc( 28 ) = ", v )           
               
        