# ===========================================================================
#
# file     : blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def blink(
    pin,
    period: int = 500_000,
    high_time = None,
    low_time = None,
    iterations = None
) -> None:
    """
    blink on the pin

    Blink on the pin with high_time and low_time
    (defaults to high_time) for the specified number of iterations
    (defaults to infinite).

    Times are in us (microseconds).
    """

    high_time = high_time or period // 2
    low_time = low_time or high_time

    p = gf.make_pin_out( pin )
    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            p.pulse( 0, 0 )
            gf.report_memory_and_time()

        p.pulse( high_time, low_time )


# ===========================================================================
