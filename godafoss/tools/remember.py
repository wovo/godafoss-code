# ===========================================================================
#
# file     : remember.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

class remember:
    """
    """

    def __init__( self, addresses ):
        self._addresses = [ address for address in addresses ]
        self._data = [ machine.mem32[ address ] for address in addresses ]

    def restore( self ):
        for address, data in zip( self._addresses, self._data ):
            machine.mem32[ address ] = data

# ===========================================================================
