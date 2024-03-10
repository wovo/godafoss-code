# ===========================================================================
#
# file     : pin_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in( gf.autoloading ):
    """
    digital input pin

    A pin_in is a digital input pin: an object from which you can
    read() a bool value.

    A pin can be negated (minus operator or inverted() function)
    to create a pin that will read the inverted level relative to the
    original pin.

    The as_pin_in() function returns the pin itself.

    The demo() function reads and prints the pin value.
    """

    # =======================================================================

    def __init__( self ):
        gf.autoloading.__init__( self, pin_in )

    # =======================================================================

    #def inverted( self ) -> "pin_in":
    #    return gf._pin_in_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "pin_in":
    #    return gf._pin_in_inverted( self )

    # =======================================================================

    def as_pin_in( self ) -> "pin_in":
        return self

    # =======================================================================

    #def demo( self, *args, **kwargs ) -> None:
    #    gf._pin_in_demo( self, *args, **kwargs )

    # =======================================================================

# ===========================================================================
