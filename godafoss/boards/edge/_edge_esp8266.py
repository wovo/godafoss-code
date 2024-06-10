# ===========================================================================
#
# file     : gf__edge_esp8266.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

class _edge_esp8266( gf._edge ):
    
    def __init__( self ):
        
        self.system = "ESP8266"
        self.pins = ( 14, 13, 12, 15, 0, 2, 5, 4 )
     
               
        