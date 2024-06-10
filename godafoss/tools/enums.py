# ===========================================================================
#
# file     : enums.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

enums = None

import godafoss as gf


# ===========================================================================

class orientation:
    north  = gf.const ( 10 )
    east   = gf.const ( 11 )
    south  = gf.const ( 12 )
    west   = gf.const ( 13 )
    
# ===========================================================================

class spi_implementation:
    "sselects a spi implementation"

    soft = gf.const ( 20 )
    "spi implemented in code (inside MicroPython)"
    
    hard = gf.const ( 21 )
    "spi implemented by the target hardware"


# ===========================================================================
