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

class _edge_esp32_lolin_c2_pico( gf._edge ):
    
    def __init__( self ):
        
        self.system = "Lolin S2 PICO"
        self.pins = ( 36, 35, 37, 34, 3, 4, 12, 17 )        
       
               
        