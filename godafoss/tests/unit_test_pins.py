# ===========================================================================
#
# file     : unit_test_pins.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_pins():
    print( "test pins" )
    unit_test_pin_dummy()
    #unit_test_pin_edge()


# ===========================================================================

def test_read( base, pin ):
        base.value = False
        assert pin.read() == False
        assert pin.inverted().read() == True

        base.value = True
        assert pin.read() == True
        assert pin.inverted().read() == False

# ===========================================================================

def test_write( base, pin ):
        pin.write( False )
        assert base.value == False

        pin.inverted().write( False )
        assert base.value == True

        pin.write( 0 )
        assert base.value == False
        pin.write( True )
        assert base.value == True
        pin.write( False )
        assert base.value == False
        pin.write( 1 )
        assert base.value == True

        pin.pulse( high_time = 1, low_time = 1 )
        gf.pulse( pin, high_time = 1, low_time = 1 )

# ===========================================================================

def test_write_oc( base, proxy ):

    proxy.write( 1 )
    assert base.is_output == False

    proxy.write( 0 )
    assert base.is_output == True
    assert base.value == False

    proxy.write( 1 )
    assert base.is_output == False

    proxy.inverted().write( 1 )
    assert base.is_output == True
    assert base.value == False

    proxy.pulse( high_time = 1, low_time = 1 )
    gf.pulse( proxy, high_time = 1, low_time = 1 )

# ===========================================================================

def test_direction( pin, proxy ):
    proxy.direction_set_input()
    assert pin.is_output == False
    proxy.direction_set_output()
    assert pin.is_output == True

# ===========================================================================

def unit_test_pin_dummy():

    d = gf.pin_in_out( None )
    assert d.as_pin_in_out() == d

    test_read( d, d )
    test_write( d, d )
    test_direction( d, d )
    test_direction( d, d.inverted() )

    di = d.as_pin_in()
    assert di.as_pin_in() == di
    assert d.is_output == False
    test_read( d, di )
    di.demo( iterations = 1, period = 1 )

    do = d.as_pin_out()
    assert do.as_pin_out() == do
    assert d.is_output == True
    test_write( d, do )
    do.demo( iterations = 1, period = 1 )

    doc = d.as_pin_oc()
    assert doc.as_pin_oc() == doc
    test_write_oc( d, doc )
    test_read( d, doc )
    test_direction( d, doc.as_pin_in_out() )

    i = doc.as_pin_in()
    assert d.is_output == False
    test_read( d, i )

    o = doc.as_pin_out()
    test_write_oc( d, o )

    io = doc.as_pin_in_out()
    test_read( d, io )
    test_write_oc( d, io )

    a = gf.pin_in_out( None )
    b = gf.pin_in_out( None )
    assert a != b
    for both in [
        sum( ( a, b ), a ),
        a + b,
        a.as_pin_out() + b,
        a + b.as_pin_out(),
        a.as_pin_out() + b.as_pin_out()
    ]:
        test_write( a, both )
        test_write( b, both )


# ===========================================================================

def unit_test_pin_edge():
    edge = gf.edge()
    a = gf.make_pin_out( edge.p0 )
    b = gf.make_pin_out( edge.p1 )
    c = gf.make_pin_in( edge.p4 )
    d = gf.make_pin_in( edge.p5 )

    a.write( 0 )
    b.write( 1 )
    assert False == c.read()
    assert True == d.read()

    a.write( 1 )
    b.write( 0 )
    assert True == c.read()
    assert False == d.read()

    both = a + b
    both.write( 0 )
    assert False == c.read()
    assert False ==d.read()
    both.write( 1 )
    assert 1 == c.read()
    assert 1 == d.read()

    a_inverted = - a
    c_inverted = - c
    a_inverted.write( False )
    assert c.read() == True
    assert c_inverted.read() == False
    a_inverted.write( True )
    assert c.read() == False
    assert c_inverted.read() == True

    a_inverted = a.inverted()
    c_inverted = c.inverted()
    a_inverted.write( False )
    assert c.read() == True
    assert c_inverted.read() == False
    a_inverted.write( True )
    assert c.read() == False
    assert c_inverted.read() == True


# ===========================================================================
