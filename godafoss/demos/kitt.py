# ===========================================================================
#
# file     : kitt.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def kitt(
    port,
    interval = 50_000,
    iterations = None
) -> None:
    """
    kitt display

    Show the Kitt on the port with the specified interval
    for the specified number of iterations
    (defaults to infinite).

    Times are in us (microseconds).
    """

    p = port.as_port_out()
    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            for n in range( 1 ):
                p.write( 0 )
                gf.sleep_us( 0 )
            gf.report_memory_and_time()

        for n in range( p.number_of_pins ):
            p.write( 0b1 << n )
            gf.sleep_us( interval )

        for n in range( p.number_of_pins - 2, 0, -1 ):
            p.write( 0b1 << n )
            gf.sleep_us( interval )

# ===========================================================================
