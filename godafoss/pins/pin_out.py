# ===========================================================================
#
# file     : pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_out( gf.autoloading ):
    """
    digital output pin

    A pin_out is a digital output pin: an object to which you can
    write() a digital level.

    A pin can be inverted (minus operator or invert() function)
    to create a pin that will write the inverted level.

    Output pins can be added together or to a port_out to create
    a (larger) port_out.

    The as_output() function returns the pin itself.

    The demo() of an output calls the global demo() function.
    """

    # =======================================================================

    def __init__( self ):
        gf.autoloading.__init__( self, pin_out )

    # =======================================================================

    #def inverted( self ) -> "_pin_out_inverted":
    #    return _gf._pin_out_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "pin_out":
    #    return _gf._pin_out_inverted( self )

    # =======================================================================

    def as_pin_out( self ) -> "pin_out":
        return self

    # =======================================================================

    def __add__( self, other ) -> "pin_out":
         return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

    #def pulse( self, *args, **kwargs ) -> None:
    #    _gf.pulse( self, *args, **kwargs )

    # =======================================================================

    #def demo( self, *args, **kwargs ):
    #    _gf.blink( self, *args, **kwargs )

    # =======================================================================

# ===========================================================================
