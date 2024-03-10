# ===========================================================================
#
# file     : invert_bits.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

def invert_bits(
    value: int,
    n_bits: int
) -> int:
    """
    the value, with its lowqer n_bits bits inverted

    :param value: int
        the value to invert

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the value, with its lower n_bits bits inverted

    This function returns the value, of which n_bits are relevant,
    with those bits inverted.
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "invert_bits example", 1 )
    """

    return ( ~ value ) & ( ( 0b1 << n_bits ) - 1 )

# ===========================================================================
