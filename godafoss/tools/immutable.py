# ===========================================================================
#
# file     : immutable.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

class immutable:
    """
    make an object immutable

    Python names are references, and class objects are mutable,
    so a class member variable can inadvertently be modified.
    The xy class is immutable, but if it were not, this would
    be possible::

        origin = xy( 0, 0 )
        a = origin
        a.x = 10 # this modifies the object that origin references!
        print( origin.x ) # prints 10

    To prevent such modifications, a value class inherits from freeze,
    and calls immutable._init__( self ) when all its members
    have been initialized.

    $macro_start immutable
    Values (objects) of this class are immutable.
    $macro_end

    usage example::
    $insert_example( "test_tools.py", "immutable example", 1 )
    """

    _frozen = False

    # =======================================================================

    def __init__( self ) -> None:
        """
        after the initialization, the object members can't be modified
        """
        self._frozen = True

    # =======================================================================

    def __delattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__delattr__( self, *args, **kwargs )

    # =======================================================================

    def __setattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__setattr__( self, *args, **kwargs )

    # =======================================================================

# ===========================================================================
