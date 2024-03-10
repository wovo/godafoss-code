# ===========================================================================
#
# file     : pin_oc__pulse.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_oc__pulse( self, *args, **kwargs ) -> None:
    gf.pulse( self, *args, **kwargs )


# ===========================================================================
