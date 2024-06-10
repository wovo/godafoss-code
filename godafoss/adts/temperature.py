# ===========================================================================
#
# file     : temperature.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class temperature( gf.immutable ):
    """
    a temperature

    :param temp: int | float
        the temperaturee, interpreted according to the scale

    :param scale: int
        the scale

    This class holds a temperature as a float.
    When constructing a temperature, or retrieveing value
    from a temperature object,
    the scale (temperature.scale.Celcius, temperature.scale.Farenheit
    or temperature.scale.Kelvin) must be specified.

    $macro_insert immutable

    examples::
    $insert_example( "test_temperature.py", "temperature examples", 1 )
    """

    class scale:
        kelvin     = "K"
        celcius    = "C"
        farenheit  = "F"

    def __init__(
        self,
        temp: int | float,
        scale: int
    ) -> None:
        self._scale = scale

        if self._scale == self.scale.kelvin:
            self._kelvin = float( temp )

        elif self._scale == self.scale.celcius:
            self._kelvin = temp + 273.15

        elif self._scale == self.scale.farenheit:
            self._kelvin = ( temp + 459.67 ) * 5 / 9

        else:
            raise ValueError

        gf.immutable.__init__( self )

    # =======================================================================

    def value(
        self,
        scale: chr
    ) -> float:
        """
        the temperature in the specified scale

        :param scale: chr
            the scale

        :result: float
            the temperature, excressed in the specified scale

        The temperature is return according to the specified scale,
        which must be one of temperature.scale.Celcius,
        temperature.scale.Farenheit or temperature.scale.Kelvin.

        This method returns the temperature in the requested scale.
        """

        if scale == self.scale.kelvin:
            return self._kelvin

        elif scale == self.scale.celcius:
            return self._kelvin - 273.15

        elif scale == self.scale.farenheit:
            return 1.8 * ( self._kelvin - 273.15) + 32

        else:
            raise ValueError

    # =======================================================================

    def __repr__( self ) -> str:
        return "%f%s" % (
            self.value( self._scale ),
            self._scale
        )
    # =======================================================================

# ===========================================================================
