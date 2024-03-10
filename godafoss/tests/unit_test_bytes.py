# ===========================================================================
#
# file     : unit_test_bytes.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def unit_test_bytes():
    print( "test bytes" )


    # bytes_from_int
    assert gf.bytes_from_int( 0, 1 ) == bytes( [ 0 ] )
    assert gf.bytes_from_int( 0, 2 ) == bytes( [ 0, 0 ] )
    assert gf.bytes_from_int( 1, 2 ) == bytes( [ 1, 0 ] )
    assert gf.bytes_from_int( 128, 2 ) == bytes( [ 128, 0 ] )
    assert gf.bytes_from_int( 256, 2 ) == bytes( [ 0, 1 ] )

    # bytes_from_int example
    assert gf.bytes_from_int( 1, 2 ) == b'\1\0'
    assert gf.bytes_from_int( 256, 2 ) == b'\0\1'
    assert gf.bytes_from_int( 258, 4 ) == b'\2\1\0\0'

    # int_from_bytes
    assert gf.int_from_bytes( bytes( [ 0 ] ) ) == 0
    assert gf.int_from_bytes( bytes( [ 0, 0, 0 ] ) ) == 0
    assert gf.int_from_bytes( bytes( [ 1, 0, 0 ] ) ) == 1
    assert gf.int_from_bytes( bytes( [ 0, 1, 0 ] ) ) == 256
    assert gf.int_from_bytes( bytes( [ 0, 0, 1 ] ) ) == 65536

    assert gf.int_from_bytes( bytes( [ 0xFF ] ) ) == 255
    assert gf.int_from_bytes( bytes( [ 0xFF ] ), signed = True ) == -1
    assert gf.int_from_bytes( bytes( [ 0x00, 0x80 ] ) ) == 0x80 * 256
    assert gf.int_from_bytes(
        bytes( [ 0x00, 0x80 ] ), signed = True ) == -32768

    # int_from_bytes example
    assert gf.int_from_bytes( b'\0' ) == 0
    assert gf.int_from_bytes( b'\1' ) == 1
    assert gf.int_from_bytes( b'\1\0' ) == 1
    assert gf.int_from_bytes( b'\0\1' ) == 256
    assert gf.int_from_bytes( b'\1\2\0' ) == 513

# ===========================================================================
