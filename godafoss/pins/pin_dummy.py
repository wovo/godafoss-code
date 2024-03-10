# ===========================================================================
#
# file     : pin_dummy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_dummy( gf.pin_in_out ):
    """
    a dummy in-out pin

    This dummy pin just sets the is_output and value properties,
    or returns the value property.
    """

    # =======================================================================

    def __init__( self ) -> None:
        gf.pin_in_out.__init__( self )
        self.value = False
        self.is_output = None

    # =======================================================================

    def direction_set_input( self ) -> None:
        self.is_output = False

    # =======================================================================

    def direction_set_output( self ) -> None:
        self.is_output = True

    # =======================================================================

    def write( self, value: bool | int ) -> None:
        self.value = bool( value )

    # =======================================================================

    def read( self ) -> bool:
        return self.value

    # =======================================================================

# ===========================================================================
