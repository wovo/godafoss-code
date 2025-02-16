# ===========================================================================
#
# file     : unit_test_basics.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_basics():
    print( "test basics" )

    # sign
    # less

    assert gf.within( 3, 2, 4 )
    assert gf.within( 2, 2, 4 )
    assert gf.within( 4, 2, 4 )
    assert not gf.within( 5, 2, 4 )
    assert not gf.within( 1, 2, 4 )

    assert gf.clamp( 1, 10, 20 ) == 10
    assert gf.clamp( 30, 10, 20 ) == 20
    assert gf.clamp( 10, 10, 20 ) == 10
    assert gf.clamp( 20, 10, 20 ) == 20
    assert gf.clamp( 15, 10, 20 ) == 15

    # make_tuple


# ===========================================================================
