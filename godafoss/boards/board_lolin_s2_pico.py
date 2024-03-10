# ===========================================================================
#
# file     : board_lolin_s2_pico.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
import machine


# ===========================================================================

class board_lolin_s2_pico:

    # =======================================================================

    def __init__( self ):
        self.button1_pin = 35
        
    # =======================================================================

    def display( self ): 
        return gf.ssd1306_i2c(
            gf.xy( 128, 32 ),
            machine.SoftI2C(
                scl = machine.Pin( 9 ),
                sda = machine.Pin( 8 )
            )    
        )
        
    # =======================================================================
        
# ===========================================================================
