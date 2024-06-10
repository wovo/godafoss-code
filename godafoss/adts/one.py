# ===========================================================================
#
# file     : one.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def one( name: str ) -> "_one":
    return _one( { name: 1 }, 1 )

# ===========================================================================

class _one( gf.immutable ):

    # =======================================================================

    def __init__(
        self,
        names: [ str ],
        value: any
    ) -> None:
        self.names = names
        self.value = value
        gf.immutable.__init__( self )

    # =======================================================================

    @staticmethod
    def _make_one(
        names: [ str ],
        value: any
    ):
        if names == {}:
            return value
        else:
            return _one( names, value )

    # =======================================================================

    @staticmethod
    def _addop(
        left: "_one",
        right: any,
        operator
    ) -> "_one":
        if not isinstance( right, _one ):
            return NotImplemented

        if left.names != right.names:
            return NotImplemented

        return _one(
            left.names,
            operator( left.value, right.value )
        )

    # =======================================================================

    @staticmethod
    def _combine_names(
        left: "_one",
        right: "_one",
        operator
    ):
        result = {}
        for name, value in left.items():
            n = operator( value, right.get( name, 0 ) )
            if n != 0:
                result[ name ] = n
        for name, value in right.items():
            n = operator( left.get( name, 0 ), value )
            if n != 0:
                result[ name ] = n
        return result

    # =======================================================================

    @staticmethod
    def _mulop(
        left: "_one",
        right: any,
        names_op,
        values_op
    ) -> any:
        if isinstance( right, _one ):
            return _one._make_one(
                _one._combine_names(
                    left.names,
                    right.names,
                    names_op
                ),
                values_op( left.value, right.value )
            )

        else:
            return _one._make_one(
                left.names,
                values_op( left.value, right )
            )

    # =======================================================================

    @staticmethod
    def _compare(
        left: "_one",
        right: any,
        compare
    ) -> bool:
        if not isinstance( right, _one ):
            return NotImplemented

        if left.names != right.names:
            return NotImplemented

        return compare( left.value, right.value )

    # =======================================================================

    def __add__(
        self,
        other: any
    ) -> any:
        return _one._addop(
            self,
            other,
            lambda a, b: a + b
        )

    # =======================================================================

    def __sub__(
        self,
        other: any
    ) -> any:
        return _one._addop(
            self,
            other,
            lambda a, b: a - b
        )

    # =======================================================================

    def __mul__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a + b,
            lambda a, b: a * b
        )

    # =======================================================================

    def __rmul__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a + b,
            lambda a, b: a * b
        )

    # =======================================================================

    def __truediv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: a / b
        )

    # =======================================================================

    def __rtruediv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: b / a
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: a // b
         )

    # =======================================================================

    def __rfloordiv__(
        self,
        other: any
    ) -> any:
        return self._mulop(
            self,
            other,
            lambda a, b: a - b,
            lambda a, b: b // a
         )

    # =======================================================================

    def __eq__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a == b
        )

    # =======================================================================

    def __lt__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a < b
        )

    # =======================================================================

    def __gt__(
        self,
        other: any
    ) -> bool:
        return _one._compare(
            self,
            other,
            lambda a, b: a > b
        )

    # =======================================================================

    def __str__( self ) -> str:
        return str( self.value ) + "*" + "".join(
            f"{name}^{self.names[name]}"
                for name in sorted( self.names )
        )

# ===========================================================================
