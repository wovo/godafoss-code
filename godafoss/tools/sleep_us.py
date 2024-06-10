# ===========================================================================
#
# file     : sleep_us.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

import time

# ===========================================================================

def sleep_us( t: int ) -> None:
    if gf.running_micropython:
        time.sleep_us( t )
    else:
        time.sleep( t / 1_000_000 )

# ===========================================================================
