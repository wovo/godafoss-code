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
    ms = ( gf.time_us() - gf.initial_time ) // 1000
    
    try:
        import gc
        gc.collect()
        free = gc.mem_free()
        b = gf.initial_free - free
        s = ", memory {b} bytes ({gf.initial_free}->{free})"
    except:
        s = ""    
    
    print( f"time {ms} ms {s}" )


# ===========================================================================
