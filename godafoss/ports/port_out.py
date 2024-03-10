# ===========================================================================
#
# file     : port_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_out( gf.autoloading ):
    """
    digital input output port

    A port_in_out is constructed from a number of pins that are
    input//outputs or can function as input//outputs.

    A port_in_out can be read or written as a whole, subject to the
    relevant pins being set to the correct direction:
    call direction_set_input() to prepare all pins
    for a read, call direction_set_output() to prepre
    all pins for a write.

    Individual pins cna be prepared for read or write by passing
    their number within the port to direction_set_input()
    or direction set_output().
    The pin value read for a pin that is output is not defined.
    A pin value written to a pin that is input might or might not
    have an effect once the pin is set to output.
    """

    # =======================================================================

    def __init__(
        self,
        number_of_pins: int,
    ) -> None:
        gf.autoloading.__init__( self, port_out )
        self.number_of_pins = number_of_pins

    # =======================================================================

    #def inverted( self ) -> "gf.port_in_out":
    #    return gf._port_out_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "gf.port_in_out":
    #    return gf._port_out_inverted( self )

    # =======================================================================

    #def mirrored( self ) -> "gf.port_in_out":
    #    return gf._port_out_mirrored( self )

    # =======================================================================

    def as_port_out( self ) -> "gf.port_out":
        return self

    # =======================================================================

# ===========================================================================

