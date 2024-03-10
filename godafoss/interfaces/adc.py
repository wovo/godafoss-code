# ===========================================================================
#
# file     : adc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class adc:
    """
    analog input

    An adc reads a voltage level and returns it
    as a fraction of the full scale.

    $macro_insert invertible

    examples::
    $insert_example( "test_adc.py", "adc examples", 1 )
    """

    # =======================================================================

    #=> def read( self ) -> "gf.fraction":
    #=>     """
    #=>     the adc value as a fraction
    #=>
    #=>     :result: :class:`~godafoss.fraction`
    #=>         adc value as a fraction of the full scale
    #=>     """
    #=>     pass

    # =======================================================================

    #=> def inverted( self ) -> "gf.adc":
    #=>     """
    #=>     the inverse of the adc
    #=>
    #=>     :result: :class:`~godafoss.adc`
    #=>         adc that returns the complement of what the
    #=>         original adc would read
    #=>
    #=>     This function returns an adc that on read() returns
    #=>     the complementof what the original adc would have read.
    #=>
    #=>     When the original adc would for example read 10/1023,
    #=>     the inverted adc reads 1013/1023.
    #=>     """
    #=>     pass

    # =======================================================================


# ===========================================================================
