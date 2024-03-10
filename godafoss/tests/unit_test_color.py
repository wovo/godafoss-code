# ===========================================================================
#
# file     : unit_test_color.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_color():
    print( "test color" )

    # attributes
    assert gf.color( 1, 2, 3 ).red == 1
    assert gf.color( 1, 2, 3 ).green == 2
    assert gf.color( 1, 2, 3 ).blue == 3
    assert gf.color( 1, 2, 3 ).rgb() == (1,2,3)

    # to string
    assert str(gf.color( 1, 2, 3 )) == '(1,2,3)'

    # clamping
    assert gf.color( 256, 2, 3 ).rgb() == (255, 2, 3)
    assert gf.color( 1, 256, 3 ).rgb() == (1, 255, 3)
    assert gf.color( 1, 2, 256 ).rgb() == (1, 2, 255)
    assert gf.color( -1, 2, 3 ).rgb() == (0, 2, 3)
    assert gf.color( 1, -1, 3 ).rgb() == (1, 0, 3)
    assert gf.color( 1, 2, -1 ).rgb() == (1, 2, 0)

    # add
    assert gf.color( 1, 2, 3 ) + gf.color( 6, 9, 13 ) \
        == gf.color(7,11,16)
    assert gf.color( 1, 1, 1 ) + gf.color( 255, 255, 255 ) \
        == gf.color(255,255,255)

    # subtract
    assert gf.color(7,11,16) - gf.color( 1, 2, 3 ) \
        == gf.color( 6, 9, 13 )
    assert gf.color( 0, 0, 0 ) - gf.color( 1, 1, 1 ) \
        == gf.color(0,0,0)

    # invert
    assert - gf.color(7,11,16) \
        == gf.color( 255-7, 255-11, 255-16 )
    assert gf.color(7,11,16).inverted() \
        == gf.color( 255-7, 255-11, 255-16 )

    # multiply
    assert 3 * gf.color(1,2,3) == gf.color( 3, 6, 9 )
    assert gf.color(1,2,3) * 3 == gf.color( 3, 6, 9 )

    # divide
    assert gf.color(10,20,30) // 3 == gf.color( 3, 6, 10 )

    # immutable
    _ = gf.color( 1, 2, 3 ).red
    try:
        gf.color( 1, 2, 3 ).red = 5
        assert False
    except:
        pass

    # color examples
    assert gf.color( 1, 2, 3 ).red == 1
    assert gf.color( 1, 2, 3 ).green == 2
    assert gf.color( 1, 2, 3 ).blue == 3
    assert gf.color( 1, 2, 3 ).rgb() == (1, 2, 3)
    assert gf.color( -100, 100, 300 ).rgb() == (0, 100, 255)
    #

    assert gf.color( 1, 2, 3 ) + gf.color( 10, 20, 30 ) \
        == gf.color( 11, 22, 33 )
    assert gf.color( 10, 20, 30 ) - gf.color( 1, 2, 3 ) \
        == gf.color( 9, 18, 27 )
    assert 10 * gf.color( 10, 20, 30 ) \
        == gf.color( 100, 200, 255 )
    assert gf.color( 10, 11, 12 ) // 2 \
        == gf.color( 5, 5, 6 )

    #
    assert str( gf.color(1,2,3) ) == "(1,2,3)"

    # color invert examples
    assert gf.color( 10, 11, 12 ).inverted() == gf.color( 245, 244, 243 )
    assert - gf.colors.white == gf.colors.black


# ===========================================================================
