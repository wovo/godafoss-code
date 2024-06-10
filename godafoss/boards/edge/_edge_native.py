# ===========================================================================
#
# file     : _edge_native.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class _edge_native( gf._edge ):
    
    def __init__( self ):
        self.system = "original RP2040 rp2 or rp2w via blinka"
        self.pins = ( 18, 19, 16, 17, 26, 27, 13 , 12 )          
               
        