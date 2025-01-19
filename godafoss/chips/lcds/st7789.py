# ===========================================================================
#
# file     : st7789.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# $$document( 0 )

import godafoss as gf


# ===========================================================================

class st7789( gf.glcd ):
    
    # =======================================================================

    def __init__( 
        self, 
        *args, **kwargs
    ):
        gf.glcd.__init__( self, *args, **kwargs )        
                   
    # =======================================================================

# ===========================================================================