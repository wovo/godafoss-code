# ===========================================================================
#
# file     : unit_test_repeater.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def count( r ):
    n = 0
    for i in r:
        n += 1
        if n >= 100:
            return n
    return n

# ===========================================================================

def unit_test_repeater():
    print( "test repeater" )

    assert count( gf.repeater( 0 )) == 0
    assert count( gf.repeater( 5 )) == 5
    assert count( gf.repeater( None )) == 100

    for n in ( 0, 1, 10 ):
        x = 0
        for _ in gf.repeater( n ):
            x += 1
        assert x == n

    x = 0
    for _ in gf.repeater( None ):
        x += 1
        if x == 100:
            break
    assert x == 100


# ===========================================================================
