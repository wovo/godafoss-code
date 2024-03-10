# ===========================================================================
#
# file     : mirror_bits.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

def mirror_bits(
    value: int,
    n_bits: int
) -> int:
    """
    the value, with its lower n_bit bits mirrored

    :param value: int
        the value to mirror

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the value, with its lower n_bits bits mirrored

    This function returns the value, of which n_bits are relevant,
    with the bits mirrored (most significant bit becomse the least
    signififacnt bit and vice verse, etc.)
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "mirror_bits example", 1 )
    """

    result = 0
    for _ in range( n_bits ):
        result = ( result << 1 ) | ( value & 0b01 )
        value = value >> 1
    return result

# ===========================================================================
