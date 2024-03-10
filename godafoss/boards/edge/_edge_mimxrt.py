# ===========================================================================
#
# file     : gf__edge_rp2.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class _edge_mimxrt( gf._edge ):
    
    def __init__( self ):
        self.system = "Teensy 4.1"
        self.pins = ( 27, 26, 1, 17, 18, 19, 20, 21 )