# ===========================================================================
#
# file     : unit_test_one.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def unit_test_one():
    print( "test one" )

    a = gf.one( "a" )
    b = 1.0 * gf.one( "b" )

    c = a + a
    d = a * b

    assert a + a == 2 * a
    assert 3 * a - a == 2 * a
    assert a < 2 * a
    assert 2 * a < a * 3
    assert 3 * a > 2 * a
    assert a * b == b * a
    assert a / a == 1
    assert b / b == 1.0
    assert 5 * a / 2 == 2.5 * a
    assert 5 * a // 2 == 2 * a
    assert 10 / ( 2 * a ) == 5 * ( 1 / a )
    assert 10 // ( 3 * a ) == 3 * ( 1 // a )

    try:
        a + 2
        assert False
    except:
        pass

    try:
        a - 3
        assert False
    except:
        pass

    try:
        a + b
        assert False
    except:
        pass

    try:
        a - b
        assert False
    except:
        pass

    try:
        a < 2
        assert False
    except:
        pass

    try:
        a > b
        assert False
    except:
        pass

    try:
        a == 2
        assert False
    except:
        pass

    try:
        a == b
        assert False
    except:
        pass

    _ = str( a )

    try:
        a.names = {}
        assert False
    except:
        pass


# ===========================================================================
