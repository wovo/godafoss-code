# ===========================================================================
#
# file     : sleep_us.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import time

# ===========================================================================

def sleep_us( t: int ) -> None:
    try:
        # MicroPython
        time.sleep_us( t )
    except:
        # native Python
        time.sleep( t / 1_000_000 )

# ===========================================================================
