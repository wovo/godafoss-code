# ===========================================================================
#
# file     : colors.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class colors:
    """
    some common color values
    """

    black   = gf.color(    0,    0,    0 )
    white   = gf.color( 0xFF, 0xFF, 0xFF )
    gray    = gf.color( 0x80, 0x80, 0x80 )

    red     = gf.color( 0xFF,    0,    0 )
    green   = gf.color(    0, 0xFF,    0 )
    blue    = gf.color(    0,    0, 0xFF )

    yellow  = gf.color( 0xFF, 0xFF,    0 )
    cyan    = gf.color(    0, 0xFF, 0xFF )
    magenta = gf.color( 0xFF,    0, 0xFF )

    violet  = gf.color( 0xEE, 0x82, 0xEE )
    sienna  = gf.color( 0xA0, 0x52, 0x2D )
    purple  = gf.color( 0x80, 0x00, 0x80 )
    pink    = gf.color( 0xFF, 0xC8, 0xCB )
    silver  = gf.color( 0xC0, 0xC0, 0xC0 )
    brown   = gf.color( 0xA5, 0x2A, 0x2A )
    salmon  = gf.color( 0xFA, 0x80, 0x72 )

# ===========================================================================
