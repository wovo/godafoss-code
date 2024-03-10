# ===========================================================================
#
# file     : pin_out__demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_out__demo( self, *args, **kwargs ):
    gf.blink( self, *args, **kwargs )


# ===========================================================================
