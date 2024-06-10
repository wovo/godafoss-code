# ===========================================================================
#
# file     : adcx__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def adcx__inverted( self ) -> "gf.adc":

    # =======================================================================

    def __init__(
        self,
        pin: gf.adc
    ):
        self._pin = pin
        gf.adc.__init__( self )

    # =======================================================================

    def read( self ) -> "gf.fraction":
        return - self._pin.read()

    # =======================================================================

    def inverted( self ) -> "gf.adc":
        return self._pin

    # =======================================================================

# ===========================================================================
