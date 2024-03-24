# ===========================================================================
#
# file     : time_us.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

import time

# ===========================================================================

def time_us() -> int:
    if gf.running_micropython:
        return time.ticks_us( t )
    else:
        return time.monotonic_ns() // 1000

# ===========================================================================
