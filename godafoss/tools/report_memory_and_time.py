# ===========================================================================
#
# file     : report_memory_and_time.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def report_memory_and_time():
    """
    report memory and time used since godafoss loading started
    """

    import time
    ms = ( time.ticks_us() - gf.initial_time ) // 1000
    
    import gc
    gc.collect()
    free = gc.mem_free()
    b = gf.initial_free - free
    
    print( f"time {ms} ms, memory {b} bytes ({gf.initial_free}->{free})" )


# ===========================================================================
