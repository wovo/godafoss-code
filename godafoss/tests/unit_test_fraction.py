# ===========================================================================
#
# file     : unit_test_fraction.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_fraction():
    print( "test fraction" )

    # attributes
    assert gf.fraction( 1, 2 ).value == 1
    assert gf.fraction( 1, 2 ).maximum == 2
    assert gf.fraction( 1, 2 ).value_maximum == (1,2)

    # clamping
    assert gf.fraction( 3, 2 ).value_maximum == (2,2)
    assert gf.fraction( -1, 2 ).value_maximum == (0,2)

    # scaled method
    assert gf.fraction( 1, 3 ).scaled( 10, 41 ) == 20
    assert gf.fraction( 1, 4 ).scaled( 10, 20 ) == 12
    assert gf.fraction( 1, 4 ).scaled( 10.0, 20 ) == 12.5
    assert gf.fraction( 1, 4 ).scaled( 10, 20.0 ) == 12.5
    assert gf.fraction( 1, 4 ).scaled( 10.0, 20.0 ) == 12.5

    # invert
    assert (-gf.fraction( 1, 4 )).value_maximum == (3,4)
    assert gf.fraction( 1, 4 ).inverted().value_maximum == (3,4)

    # to string
    assert str(gf.fraction( 1, 4 )) == '(1/4)'

    # immutable
    _ = gf.fraction( 1, 3 ).value
    try:
        gf.fraction( 1, 3 ).value = 5
        assert False
    except:
        pass

    # fraction examples
    assert gf.fraction( 1, 2 ).value == 1
    assert gf.fraction( 1, 2 ).maximum == 2

    # fraction scaled examples
    assert gf.fraction( 1, 3 ).scaled( 10, 40 ) == 20
    assert gf.fraction( 1, 4 ).scaled( 10, 20 ) == 12
    assert gf.fraction( 1, 4 ).scaled( 10.0, 20 ) == 12.5

    # fraction invert examples
    assert gf.fraction( 1, 3 ).inverted() == gf.fraction( 2, 3 )
    assert - gf.fraction( 1, 3 ) == gf.fraction( 2, 3 )

# ===========================================================================
