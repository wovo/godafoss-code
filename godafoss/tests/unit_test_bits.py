# ===========================================================================
#
# file     : unit_test_bits.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def unit_test_bits():
    print( "test bits" )

    unit_test_bar_bits()
    unit_test_invert_bits()
    unit_test_mirror_bits()

# ===========================================================================

def unit_test_bar_bits():

    assert gf.bar_bits( 0 ) == 0x00
    assert gf.bar_bits( 1 ) == 0x01
    assert gf.bar_bits( 7 ) == 0x7F
    assert gf.bar_bits( 8 ) == 0xFF

    # bar_bits
    assert gf.bar_bits( 0 ) == 0b0
    assert gf.bar_bits( 1 ) == 0b1
    assert gf.bar_bits( 4 ) == 0b1111
    assert gf.bar_bits( 32 ) == 0b11111111111111111111111111111111

    # bar_bits example
    assert gf.bar_bits( 0 ) == 0b0
    assert gf.bar_bits( 4 ) == 0b1111

# ===========================================================================

def unit_test_invert_bits():

    assert gf.invert_bits( 0x01, 8 ) == 0xFE
    assert gf.invert_bits( 0x05, 6 ) == 0x3A

    assert gf.invert_bits( 0b0, 8 ) == 0b11111111
    assert gf.invert_bits( 0b1, 1 ) == 0b0
    assert gf.invert_bits( 0b1, 8 ) == 0b11111110
    assert gf.invert_bits( 0b1110011, 7 ) == 0b0001100

    # invert_bits example
    assert gf.invert_bits( 0b111010, 6 ) == 0b101
    assert gf.invert_bits( 0b101010, 10 ) == 0b1111010101

# ===========================================================================

def unit_test_mirror_bits():

    assert gf.mirror_bits( 0x01, 8 ) == 0x80
    assert gf.mirror_bits( 0x03, 4 ) == 0x0C

    assert gf.mirror_bits( 0b0, 8 ) == 0b0
    assert gf.mirror_bits( 0b1, 8 ) == 0b10000000
    assert gf.mirror_bits( 0b1110011, 7 ) == 0b1100111
    assert gf.mirror_bits( 0b00101000, 8 ) == 0b00010100
    assert gf.mirror_bits( 0b00100100, 8 ) == 0b00100100

    # mirror_bits example
    assert gf.mirror_bits( 0b111010, 6 ) == 0b10111
    assert gf.mirror_bits( 0b1, 4 ) == 0b1000

# ===========================================================================
