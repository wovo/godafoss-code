# ===========================================================================
#
# file     : font_default.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class font_default( gf.autoloading, gf.font ):
    """
    the micropython built-in 8x8 font
    """

    def __init__( self ):
        gf.autoloading.__init__( self, font_default )
        gf.font.__init__( self, gf.xy( 8, 8 ) )


# ===========================================================================
