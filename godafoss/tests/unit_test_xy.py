# ===========================================================================
#
# file     : unit_test_xy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_xy():
    print( "test xy" )

    # attributes
    assert gf.xy( 1, 2 ).x == 1
    assert gf.xy( 1, 2 ).y == 2
    assert gf.xy( 1, 2 ).xy == ( 1, 2 )
    assert str(gf.xy( 1, 2 )) == '(1,2)'

    # comparing
    assert gf.xy( 1, 2 ) == gf.xy( 1, 2 )
    assert gf.xy( 1, 2 ) != gf.xy( 1, 3 )
    assert gf.xy( 1, 2 ) != gf.xy( 2, 2 )
    assert gf.xy( 1, 2 ) != gf.xy( 2, 1 )

    # add, subtract
    assert gf.xy( 1, 2 ) + gf.xy( 3, 7 ) == gf.xy( 4, 9 )
    assert gf.xy( 1, 2 ) - gf.xy( 3, 7 ) == gf.xy( -2, -5 )

    # negative
    assert - gf.xy( 3, 7 ) == gf.xy( -3, -7 )

    # multiply
    assert 3 * gf.xy( 1, 2 ) == gf.xy( 3, 6 )
    assert gf.xy( 1, 2 ) * 5 == gf.xy( 5, 10 )
    try:
        gf.xy( 1, 2 ) * 5.0
        assert False
    except NotImplementedError:
        pass
    except TypeError:
        pass


    # true division
    assert gf.xy( 12, 7 ) // 3 == gf.xy( 4, 2 )

    # immutable
    _ = gf.xy( 1, 2 ).x
    try:
        gf.xy( 1, 2 ).x = 5
        assert False
    except:
        pass

    # xy examples
    assert gf.xy( 1, 2 ).x == 1
    assert gf.xy( 1, 2 ).y == 2
    assert gf.xy( 1, 2 ).xy == ( 1, 2 )

    assert gf.xy( 1, 2 ) + gf.xy( 10, 30 ) == gf.xy( 11, 32 )
    assert gf.xy( 10, 20 ) - gf.xy( 4, 9 ) == gf.xy( 6, 11 )
    assert 2 * gf.xy( 1, 2 ) == gf.xy( 2, 4 )
    assert gf.xy( 4, 9 ) // 2 == gf.xy( 2, 4 )
    assert str( gf.xy( 1, 2 ) ) == "(1,2)"




# ===========================================================================
