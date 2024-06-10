# ===========================================================================
#
# file     : int_from_bytes.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def int_from_bytes(
    array: bytes | bytearray,
    signed: bool = False
) -> int:
    """int value from a lowest-byte-first sequence of bytes

    :param array: bytes | bytearray
        the array of bytes that is to be converted to an integer

    :param signed: bool
        treat the resulting bit pattern as unsigned (False, default)
        or signed (True)

    :result: int
        the array interpreted as integer value

    This function returns the bytes as an unsigned integer value,
    the first byte as least significant byte of the int value.

    Python has the int.from_bytes function, but it is currently
    not implemented fully and correctly in MicroPython.
    Hence this alternative.

    examples
    $insert_example( "test_tools.py", "int_from_bytes example", 1 )
    """

    result = 0
    for i in range( len( array ) - 1, -1, -1 ):
        result = ( result << 8 ) | ( array[ i ] & 0xFF )

    if signed and ( ( array[ -1 ] & 0x80 ) != 0 ):
        result = - ( ( result - 1 ) ^ gf.bar_bits( 8 * len( array ) ) )

    return result

# ===========================================================================

