# ===========================================================================
#
# file     : elapsed_us.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def elapsed_us( f, *args, **kwargs ):
    """
    time a function call

    This function calls the function f with the provided parameters
    and returns the elapsed time in microseconds
    """

    before = gf.ticks_us()
    f( *args, *kwargs )
    after = gf.ticks_us()
    return after - before

# ===========================================================================
