# ===========================================================================
#
# file     : bytes_from_int.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

def bytes_from_int(
    value: int,
    n_bytes: int
) -> bytes:
    """bytes lsb-first representation of an int

    :param value: int
        the value to be converted to bytes

    :param n_bytes: int
        the desired number of bytes

    :result: bytes
        the bytes representation of the value

    This function returns the int value as n_byte bytes,
    least significant byte first (little endian).

    examples::
    $insert_example( "test_tools.py", "bytes_from_int example", 1 )
    """

    array = bytearray( n_bytes )
    for i in range( 0, n_bytes ):
        array[ i ] = value & 0xFF
        value = value >> 8
    return bytes( array )

# ===========================================================================
