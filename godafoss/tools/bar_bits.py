# ===========================================================================
#
# file     : bar_bits.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

def bar_bits(
    n_bits: int
) -> int:
    """
    unsigned int value with (only) the lower n_ones bits 1

    :param n_bits: int
        the number of 1-value bits in the result

    :result: int
        unsigned int value, with (only) the lower n_bits bits 1

    This function returns the integer value,
    of which the lowest n_ones bits
    are 1 (set), the other (higher) bits are 0 (clear).

    examples
    $insert_example( "test_tools.py", "bar_bits example", 1 )
    """

    result = 0
    for _ in range( n_bits ):
        result = ( result << 1 ) | 0b1
    return result

# ===========================================================================
