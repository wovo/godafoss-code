# ===========================================================================
#
# file     : pulse.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pulse(
    pin, # : int | "gf.pin_in_out" | "gf.pin_out" | "gf.pin_oc",
    high_time: int,
    low_time: int = 0
) -> None:
    """
    high pulse on the pin

    The pin is used to make a pin_out.

    Make the pin high, wait for high_time (must be provided),
    make the pin low, and wait for low_time (defaults to zero).

    Times are in us (microseconds).
    """

    pin = gf.make_pin_out( pin )

    pin.write( True )
    if high_time != 0:
        gf.sleep_us( high_time )

    pin.write( False )
    if low_time != 0:
        gf.sleep_us( low_time )

# ===========================================================================
