# ===========================================================================
#
# file     : unit_test_temperature.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

def close( v1, v2, abs_tol = None ):
    import math
    if abs_tol is None:
        assert math.isclose( v1, v2, rel_tol = 0.001 )
    else:
        assert math.isclose( v1, v2, abs_tol = abs_tol )

# ===========================================================================

def unit_test_temperature():
    print( "test temperature" )

    # kelvin
    k0 = gf.temperature( 0, gf.temperature.scale.kelvin )
    close( k0.value( gf.temperature.scale.kelvin ), 0 )
    close( k0.value( gf.temperature.scale.celcius ), -273.15 )
    close( k0.value( gf.temperature.scale.farenheit ), -459.67 )
    assert str(k0) == ( "%fK" % 0.0 )

    k300 = gf.temperature( 300, gf.temperature.scale.kelvin )
    close( k300.value( gf.temperature.scale.kelvin ), 300 )
    close( k300.value( gf.temperature.scale.celcius ), 26.85 )
    close( k300.value( gf.temperature.scale.farenheit ), 80.33 )
    assert str(k300) == ( "%fK" % 300.0 )

    # celcius
    c0 = gf.temperature( 0, gf.temperature.scale.celcius )
    close( c0.value( gf.temperature.scale.kelvin ), 273.15 )
    close( c0.value( gf.temperature.scale.celcius ), 0 )
    close( c0.value( gf.temperature.scale.farenheit ), 32.0 )
    assert str(c0) == ( "%fC" % 0.0 )

    c300 = gf.temperature( 300, gf.temperature.scale.celcius )
    close( c300.value( gf.temperature.scale.kelvin ), 573.15 )
    close( c300.value( gf.temperature.scale.celcius ), 300 )
    close( c300.value( gf.temperature.scale.farenheit ), 572.0 )
    assert str(c300) == ( "%fC" % 300.0 )

    # farenheit
    f0 = gf.temperature( 0, gf.temperature.scale.farenheit )
    close( f0.value( gf.temperature.scale.kelvin ), 255.372 )
    close( f0.value( gf.temperature.scale.celcius ), -17.78 )
    close( f0.value( gf.temperature.scale.farenheit ), 0, abs_tol = 0.0001 )
    assert str(f0) == ( "%fF" % 0.0 )

    f300 = gf.temperature( 300, gf.temperature.scale.farenheit )
    close( f300.value( gf.temperature.scale.kelvin ), 422.039 )
    close( f300.value( gf.temperature.scale.celcius ), 148.889 )
    close( f300.value( gf.temperature.scale.farenheit ), 300.0 )
    assert str(f300) == ( "%fF" % 300.0 )

    # scale validity check
    for c in range( 0, 255 ):
        c = chr( c )
        if not c in [ "C", "F", "K" ]:
            try:
                k0.value( "d" )
                assert False
            except:
                pass

            try:
                gf.temperature( 0, c )
                assert False
            except:
                pass
        else:
            k0.value( c )
            gf.temperature( 0, c )


    # immutable
    try:
        k0.x = 5
        assert False
    except:
        pass

    # temperature examples
    k0 = gf.temperature( 0, gf.temperature.scale.kelvin )
    close( k0.value( gf.temperature.scale.kelvin ), 0 )
    close( k0.value( gf.temperature.scale.celcius ), -273.15 )
    assert str( k0 ) == ( "%fK" % 0.0 )
    #
    c0 = gf.temperature( 0, gf.temperature.scale.celcius )
    close( c0.value( gf.temperature.scale.kelvin ), 273.15 )
    close( c0.value( gf.temperature.scale.celcius ), 0 )
    assert str( c0 ) == ( "%fC" % 0.0 )
    #
    f32 = gf.temperature( 32, gf.temperature.scale.farenheit )
    close( f32.value( gf.temperature.scale.celcius ), 0.00 )
    assert str( f32 ) == ( "%fF" % 32.0 )
    f212 = gf.temperature( 212, gf.temperature.scale.farenheit )
    close( f212.value( gf.temperature.scale.celcius ), 100.00 )





# ===========================================================================
