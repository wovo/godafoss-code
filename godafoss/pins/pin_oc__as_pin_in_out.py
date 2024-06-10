# ===========================================================================
#
# file     : pin_oc__as_pin_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def pin_oc__as_pin_in_out( self ):
    """
    the input-output version of the pin

    Note that is a pseudo (input-) output: writing a zero to
    it will pull the output low, but writing a one to it will float
    the output (not pull it high, as a read input-output pin would).
    """

    class _as_pin_in_out( gf.pin_in_out ):

        # ===================================================================

        def __init__( self, pin ) -> None:
            gf.pin_in_out.__init__( self, self )
            self._pin = pin

        # ===================================================================

        def direction_set_input( self ) -> None:
            self._pin.write( 1 )

        # ===================================================================

        def direction_set_output( self ) -> None:
            # It is debatable whether this is needed, but
            # it makes testing more regular.
            self._pin.write( 0 )

        # ===================================================================

        def write( self, value ) -> None:
            self._pin.write( value )

        # ===================================================================

        def read( self ):
            return self._pin.read()

    # =======================================================================

    return _as_pin_in_out( self )

# ===========================================================================

