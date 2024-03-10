# ===========================================================================
#
# file     : dac.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class dac:
    """
    an analog output pin

    A write causes a dac to output the specified voltage.
    The value written is a fraction of the full scale output.

    $macro_insert invertible

    examples::
    $insert_example( "test_dac.py", "dac examples", 1 )
    """

    # =======================================================================

    def __init__( self ) -> None:
        invertible.__init__( self )

    # =======================================================================

    def write(
        self,
        value: gf.fraction
    ) -> None:
        """
        write the adc value as a fraction

        :param value: :class:`~godafoss.fraction`
            value as a fraction of te full scale
        """
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "gf.dac":
        """
        dac that outputs the negative (complement) of the written value

        :result: :class:`~godafoss.dac`
            dac that, when written to, writes the complement of that value
            to the original dac

        This function returns a dac that outputs the negative
        (complement) of the written value to the original dac.

        examples::
        $insert_example( "test_dac.py", "dac invert examples", 2 )
        """

        return _gf._dac_inverted( self )

    # =======================================================================

# ===========================================================================


class _dac_inverted( dac ):
    """proxy that inverts a dac"""

    # =======================================================================

    def __init__( self, pin: dac ) -> None:
        self._pin = pin
        dac.__init__( self )

    # =======================================================================

    def write( self, value: gf.fraction ) -> None:
        self._pin.write( - value )

    # =======================================================================

    def inverted( self ) -> dac:
        return self._pin

    # =======================================================================

# ===========================================================================
