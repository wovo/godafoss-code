# ===========================================================================
#
# file     : pin_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out( gf.autoloading ):
    """
    digital input output pin

    A pin_in_out is a digital input output pin.

    The direction can be set to input or output by the
    direction_set_input() and direction_set_output() functions.

    When the direction is output, the pin level can be written.

    When the direction is input, the pin level can be read.

    A pin can be inverted (minus operator or inverted() function)
    to create a pin that will read and write the inverted level.

    Input output pins can be added together or to a port_in_out to create
    a (larger) port_in_out.

    The as_pin_in_out() function returns the pin itself.

    The as_pin_in() function returns the input-only version of the pin.

    The as_pin_out() function returns the output-only version of the pin.

    The as_pin_oc() function returns the open-collector version of the pin.
    """

    # =======================================================================

    def __init__( self ):
        gf.autoloading.__init__( self, pin_in_out )

    # =======================================================================

    #def inverted( self ) -> "pin_in_out":
    #    return gf._pin_in_out_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "pin_in_out":
    #    return self.inverted()

    # =======================================================================

    def as_pin_in_out( self ) -> "pin_in_out":
        return self

    # =======================================================================

    #def as_pin_out( self ) -> "pin_out":
    #    return gf.pin_in_out__as_pin_out( self )

    # =======================================================================

    #def as_pin_in( self ) -> "pin_in":
    #    return gf.pin_in_out__as_pin_in( self )

    # =======================================================================

    #def as_pin_oc( self ) -> "pin_oc":
    #    return gf.pin_in_out__as_pin_oc( self )

    # =======================================================================

    def __add__( self, other ) -> "pin_out":
         return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

    #def pulse( self, *args, **kwargs ) -> None:
    #    _gf.pulse( self, *args, **kwargs )

    # =======================================================================

# ===========================================================================
