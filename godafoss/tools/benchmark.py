# ===========================================================================
#
# file     : benchmark.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# inspired by similar code on the micropython website

def benchmark( function, *args, **kwargs ):
    """
    decorator for benchmarking

    This function decorator will report the time spent (in microseconds)
    and memory claimed (in bytes) each time the decorated function runs.
    """

    function_name = str( f ).split( ' ' )[ 1 ]

    # local to avoid loading these modules
    # when this decorator is not used
    from godafoss.gf_gc import collect, mem_free
    from godafoss.gf_time import ticks_us

    def new_function( *args, **kwargs ):

        collect()
        before_bytes = mem_free()
        before_us = ticks_us()

        result = f( *args, **kwargs )

        after_us = ticks_us()
        collect()
        after_bytes = mem_free()

        print( "%s took %d us, claimed %d bytes" % (
            function_name,
            after_us - before_us,
            before_bytes - after_bytes
        ) )

        return result

    return new_function
