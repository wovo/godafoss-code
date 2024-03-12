# ===========================================================================
#
# file     : always.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in this file
#
# ===========================================================================
#
# These things are always loaded, bypassing the on-demand loading machanism.
#
# ===========================================================================


# ===========================================================================

def all( first, *args ):
    return first.combine( *args )

# ===========================================================================

def sign( x ):
   return 1 if x > 0 else -1 if x < 0 else 0

# ===========================================================================

def less( x, n = 1 ):
   return x - sign( x ) * n

# ===========================================================================

def within(
    a: any,
    low: any,
    high: any
) -> bool:
    """
    test whether a value is between two bounds

    :param a: any
        the value to be checked

    :param low: any
        the lower bound to check the value against

    :param high: any
        the higher bound to check the value against

    :result: any
        whether a is in the trange [low..high]

    This function returns whether a is between low and high.
    The low and high values are included in the allowed range.

    Low and high must be in order: low =< high.
    If they are not the function will return False.

    examples::
    $insert_example( "test_tools.py", "within example", 1 )
    """
    return ( a >= low ) and ( a <= high )

# ===========================================================================

def clamp(
    x: any,
    low: any,
    high: any
) -> any:
    """
    x, clamped to the nearest value in the range [low..high]

    :param x: any
        the value to clamp within the range [low..high]

    :param low: any
        the lower bound of the clamp interval

    :param high: any
        the higher bound of the clamp interval

    :result: any
        either x, or the nearest value in the range [low..high]

    This function returns max( low, min( x, high ) ).

    examples::
    $insert_example( "test_tools.py", "clamp example", 1 )
    """

    return max( low, min( x, high ) )


# ===========================================================================

def make_tuple(
    *args: any
) -> any:
    """
    make a tuple from a tuple or list, or from a number of arguments

    :param \*args: any
        the arguments are to be turned into a tuple

    :result: any
        a tuple constructed from the \*args

    When called with one argument, which is a list or a tuple,
    this function returns it as a tuple.
    Otherwise, it returns a tuple of its argument(s).

    examples::
    $insert_example( "test_tools.py", "make_tuple example", 1 )
    """

    if len( args ) == 1 and isinstance( args[ 0 ], ( list, tuple ) ):
        return tuple( args[ 0 ] )
    else:
        return tuple( args )


# ===========================================================================

