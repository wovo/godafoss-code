# ===========================================================================
#
# file     : adc__read.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def adc__read( self ) -> "gf.fraction":
    """
    Read and return the adc value as a fraction of its full scale.
    """

    raise NotImplementedError

# ===========================================================================
