# ===========================================================================
#
# file     : pin_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_oc( gf.autoloading ):
    """
    open-collector input output pin

    A pin_oc is an open-collector (or more likely, open-drain)
    digital input output pin.

    The pin level can be written.
    When a 0 is written, the pin hardware will pull the output level low.
    When a 1 is written, the pin hardware will let the pin level float.

    The pin level can be read.
    When a 0 has been written to the pin, a 0 will be read unless
    there is some serious hardware trouble.
    When a 1 has been written, the level on the pin will be read.

    A pin can be negated to create a pin that will read and write
    the inverted level.

    The as_pin_in function returns the input-only version of the pin.

    The as_pin_out function returns the output-only version of the pin.

    The as_pin_in_out function returns the input-output version
    of the pin. Note that is a pseudo input-output: writing a zero to
    it will pull the output low, but writing a one to it will float
    the output (not pull it high, as a read input-output pin would).

    The as_pin_oc function returns the pin itself.

    Open collector pins can be added together or to a port_oc to create
    a (larger) port_oc.
    """

    # =======================================================================

    def __init__( self ):
        gf.autoloading.__init__( self, pin_oc )

    # =======================================================================

    #def inverted( self ) -> "pin_oc":
    #    return gf._pin_oc_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "pin_oc":
    #    return gf._pin_oc_inverted( self )

    # =======================================================================

    #def as_pin_in( self ) -> "pin_in":
    #    return gf._pin_oc_as_pin_in( self )

    # =======================================================================

    #def as_pin_out( self ) -> "pin_out":
    #    return gf._pin_oc_as_pin_out( self )

    # =======================================================================

    #def as_pin_in_out( self ) -> "pin_in_out":
    #    return gf._pin_oc_as_pin_in_out( self )

    # =======================================================================

    def __add__( self, other ) -> "pin_out":
         return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

    #def pulse( self, *args, **kwargs ) -> None:
    #    _gf.pulse( self, *args, **kwargs )

    # =======================================================================

    def as_pin_oc( self ) -> "pin_oc":
        return self

    # =======================================================================

# ===========================================================================
