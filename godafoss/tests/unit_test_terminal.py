# ===========================================================================
#
# file     : unit_test_terminal.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def unit_test_terminal():
    print( "test terminal" )

    t = gf.terminal_dummy( gf.xy( 20, 4 ) )
    #print( t.lines() )
    assert t.lines() == [
        "********************",
        "********************",
        "********************",
        "********************",
    ]

    t.clear()
    #print( t.lines() )
    assert t.lines() == [
        "                    ",
        "                    ",
        "                    ",
        "                    ",
    ]

    t.clear( '.' )
    #print( t.lines() )
    assert t.lines() == [
        "....................",
        "....................",
        "....................",
        "....................",
    ]

    t.clear( '.' )
    t.write( "Hello\nworld" )
    #print( t.lines() )
    assert t.lines() == [
        "Hello...............",
        "world...............",
        "....................",
        "....................",
    ]

    t.clear( '.' )
    t.write( "AA\fHi\n here\rt" )
    #print( t.lines() )
    assert t.lines() == [
        "Hi                  ",
        "there               ",
        "                    ",
        "                    ",
    ]

    t.clear( '.' )
    t.write( "BLAlo\vHel\nworld" )
    #print( t.lines() )
    assert t.lines() == [
        "Hello...............",
        "world...............",
        "....................",
        "....................",
    ]

    t.clear( '.' )
    t.write( "\t0502XyZ" )
    #print( t.lines() )
    assert t.lines() == [
        "....................",
        "....................",
        ".....XyZ............",
        "....................",
    ]

    t.clear( '.' )
    t.write( "This line is much too long" )
    t.write( "\n1\n2\nlast line\nbeyond the bottom" )
    #print( t.lines() )
    assert t.lines() == [
        "This line is much to",
        "1...................",
        "2...................",
        "last line...........",
    ]

# ===========================================================================
