# ===========================================================================
#
# file     : pcf8574.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf



class pcf8574( gf._pcf8574x ):
    
    def __init__(
        self,
        bus,
        address = 0
    ):
        """
        create a pcf8574 interface
        
        The address must be the 3 bits formed by A0 .. A2.
        """    
        gf.pcf8574x.__init__( self, bus, 0x20 + address )


# ===========================================================================
