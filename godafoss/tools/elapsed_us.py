# ===========================================================================
#
# file     : elapsed_us.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

def elapsed_us( f, *args, **kwargs ):
    """
    time a function call

    This function callss the function f with the provided parameters
    and returns the elapsed time in microseconds
    """

    from godafoss.gf_time import ticks_us

    before = ticks_us()
    f( *args, *kwargs )
    after = ticks_us()
    return after - before

# ===========================================================================
