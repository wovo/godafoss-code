# ===========================================================================
#
# file     : unit_test_xyz.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_xyz():
    print( "test xyz" )

    # attributes
    assert gf.xyz( 1, 2, 3 ).x == 1
    assert gf.xyz( 1, 2, 3 ).y == 2
    assert gf.xyz( 1, 2, 3 ).z == 3
    assert gf.xyz( 1, 2, 3 ).xyz == ( 1, 2, 3 )

    # to string
    assert str(gf.xyz( 1, 2, 3 )) == '(1,2,3)'

    # comparing
    assert gf.xyz( 1, 2, 3 ) == gf.xyz( 1, 2, 3 )
    assert gf.xyz( 1, 2, 3 ) != gf.xyz( 1, 2, 4 )
    assert gf.xyz( 1, 2, 3 ) != gf.xyz( 1, 3, 3 )
    assert gf.xyz( 1, 2, 3 ) != gf.xyz( 2, 2, 3 )
    assert gf.xyz( 1, 2, 3 ) != gf.xyz( 3, 2, 1 )

    # add, subtract
    assert gf.xyz( 1, 2, 3 ) + gf.xyz( 11, 15, 19) == gf.xyz( 12, 17, 22 )
    assert gf.xyz( 1, 2, 3 ) - gf.xyz( 11, 15, 19) == gf.xyz( -10, -13, -16 )

    # negative
    assert - gf.xyz( 3, 7, 19 ) == gf.xyz( -3, -7, -19 )

    # multiply
    assert 3 * gf.xyz( 1, 2, 7 ) == gf.xyz( 3, 6, 21 )
    assert gf.xyz( 1, 2, 7 ) * 3 == gf.xyz( 3, 6, 21 )

    # divide
    assert gf.xyz( 12, 7, 31 ) // 3 == gf.xyz( 4, 2, 10 )
    assert gf.xyz( 12, 7, 31 ) / 2 == gf.xyz( 6, 3.5, 15.5 )

    # immutable
    _ = gf.xyz( 1, 2, 3 ).x
    try:
        gf.xyz( 1, 2, 3 ).x = 5
        assert False
    except:
        pass

    # xyz examples
    assert gf.xyz( 1, 2, 3 ).x == 1
    assert gf.xyz( 1, 2, 3 ).y == 2
    assert gf.xyz( 1, 2, 3 ).z == 3
    assert gf.xyz( 1, 2, 3 ).xyz == (1,2,3)

    #
    assert gf.xyz( 1, 2, 3 ) + gf.xyz( 10, 30, 100) == gf.xyz( 11, 32, 103 )
    assert gf.xyz( 10, 20, 30 ) - gf.xyz( 4, 9, 15 ) == gf.xyz( 6, 11, 15 )
    assert 2 * gf.xyz( 1, 2, 3 ) == gf.xyz( 2, 4, 6 )
    assert gf.xyz( 4, 9, 12 ) // 2 == gf.xyz( 2, 4, 6 )
    assert str( gf.xyz( 1, 2, 3 ) ) == "(1,2,3)"




# ===========================================================================
