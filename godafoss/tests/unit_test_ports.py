# ===========================================================================
#
# file     : unit_test_ports.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_ports():
    print( "test ports" )
    unit_test_port_dummy()
    unit_test_port_pins()


# ===========================================================================

def test_read( base, port ):

    base.values = 0x25
    assert port.read() == 0x25
    assert port.mirrored().read() == 0xA4
    assert port.inverted().read() == 0xDA
#    assert ( - port ).read() == 0xDA


# ===========================================================================

def test_write( base, port ):
    port.write( 0x5A )
    assert base.values == 0x5A

    port.mirrored().write( 0x28 )
    assert base.values == 0x14

    port.inverted().write( 0x28 )
    assert base.values == 0xD7

#    ( - port ).write( 0x12 )
#    assert base.values == 0xED


# ===========================================================================

def test_write_oc( base, proxy ):

    proxy.write( 0x39 )
    assert base.directions == 0x39
    assert base.values == 0x39

    proxy.inverted().write( 0x85 )
    assert base.directions == 0x7A
    assert base.values == 0x7A

#    ( - proxy ).write( 0x11 )
#    assert base.directions == 0xEE
#    assert base.values == 0xEE

    proxy.mirrored().write( 0x28 )
    assert base.directions == 0x14
    assert base.values == 0x14


# ===========================================================================

def test_direction( port, proxy ):

    proxy.direction_set_input()
    assert port.directions == 0xFF

    proxy.direction_set_output()
    assert port.directions == 0x00

    proxy.directions_set( 0x53 )
    assert port.directions == 0x53

    proxy.inverted().directions_set( 0x11 )
    assert port.directions == 0x11

    proxy.mirrored().directions_set( 0x12 )
    assert port.directions == 0x48

# ===========================================================================

def unit_test_port_dummy():
    d = gf.port_buffer( 8 )
    assert d.as_port_in_out() == d

    test_read( d, d )
    test_write( d, d )
    test_direction( d, d )

    do = d.as_port_out()
    do.as_port_out() == d
    assert d.directions == 0x00
    test_write( d, do )

    di = d.as_port_in()
    di.as_port_in() == di
    assert d.directions == 0xFF
    test_read( d, di )

    doc = d.as_port_oc()
    doc.as_port_oc() == doc
    test_read( d, doc )
    test_write_oc( d, doc )

    di = doc.as_port_in()
    test_read( d, di )

    do = doc.as_port_out()
    test_write_oc( d, do )

    dio = doc.as_port_in_out()
    test_read( d, dio )
    test_write_oc( d, dio )
    test_direction( d, dio )


# ===========================================================================

def unit_test_port_pins():
    pins = [
        gf.pin_in_out( None ),
        gf.pin_in_out( None ),
        gf.pin_in_out( None ),
        gf.pin_in_out( None ),
    ]
    port = gf.make_port_in_out( pins )
    port.write( 0x03 )
    assert pins[ 0 ].value == True
    assert pins[ 1 ].value == True
    assert pins[ 2 ].value == False
    assert pins[ 3 ].value == False
    assert port.read() == 0x03

    try:
        _ = gf.make_port_in_out( "hello" )
        assert False
    except:
        pass

    port.directions_set( 0x02 )
    assert pins[ 0 ].is_output == True
    assert pins[ 1 ].value == True
    assert pins[ 2 ].value == False
    assert pins[ 3 ].value == False


# ===========================================================================
