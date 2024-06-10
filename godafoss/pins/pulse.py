# ===========================================================================
#
# file     : pulse.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pulse(
    pin: "int | str | can_pin_out",
    high_time: int,
    low_time: int = 0
) -> None:
    """
    $$see_also( "pin_out" )
    
    make the pin high, wait for high_time,
    make the pin low, and wait for low_time
    
    $$insert_image( "pulse", 300 )

    :param pin: (int|str|can_pin_out) 
        pin (converted to 
        $$class( "pin_out" ) 
        to output the pulse on

    :param high_time: (int) 
        duration of the high part of the pulse

    :param low_time: (int) 
        duration of the low part of the pulse (defaults to 0)

    The times are in us (microseconds).
    """

    pin = gf.pin_out( pin )

    pin.write( True )
    if high_time != 0:
        gf.sleep_us( high_time )

    pin.write( False )
    if low_time != 0:
        gf.sleep_us( low_time )

# ===========================================================================
