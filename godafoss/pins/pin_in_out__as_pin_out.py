# ===========================================================================
#
# file     : pin_in_out__as_pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_in_out__as_pin_out( self ) -> "gf.pin_out":
    """
    the output-only version of the pin

    Note that is a pseudo output: writing a zero to
    it will pull the output low, but writing a one to it will float
    the output (not pull it high, as a read input-output pin would).
    """

    # =======================================================================

    class _as_pin_out( gf.pin_out ):

        # ===================================================================

        def __init__(
            self,
            pin: "gf.pin_in_out"
        ) -> None:
            self._pin = pin
            self._pin.direction_set_output()

            # speed things up and save some RAM ...
            self.write = self._pin.write

            gf.pin_out.__init__( self, self )

        # ===================================================================

    # =======================================================================

    return _as_pin_out( self )

# ===========================================================================
