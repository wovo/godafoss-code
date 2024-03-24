# ===========================================================================
#
# file     : no_new_attributes.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

class no_new_attributes:
    """
    make it impossible to add new attributes

    In an object that inherits from this class can (after the
    no_new_attributes.__init__() call) no new attributes can be created.
    This can be usefull to prevent accidentally setting an
    attributeb that is spelled wrong.
    """

    _no_new = False

    # =======================================================================

    def __init__( self ) -> None:
        """
        after the initialization, no new attributes can be created
        """
        self._no_new = True

    # =======================================================================

    def __setattr__( self, name, value ):
        if self._no_new:
            _ = eval( f"self.{name}" )
        object.__setattr__( self, name, value )

    # =======================================================================

# ===========================================================================
