# ===========================================================================
#
# file     : port_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

class port_oc( gf.autoloading ):
    """
    """

    # =======================================================================

    def __init__(
        self,
        number_of_pins: int,
    ) -> None:
        gf.autoloading.__init__( self, port_oc )
        self.number_of_pins = number_of_pins

    # =======================================================================

    #def inverted( self ) -> "gf.port_oc":
    #    return gf._port_oc_inverted( self )

    # =======================================================================

    #def __neg__( self ) -> "gf.port_oc":
    #    return gf._port_oc_inverted( self )

    # =======================================================================

    #def mirrored( self ) -> "gf.port_oc":
    #    return gf._port_oc_mirrored( self )

    # =======================================================================

    #def as_port_in( self ) -> "gf.port_in":
    #    return gf._port_oc_as_port_in( self )

    # =======================================================================

    #def as_port_out( self ) -> "gf.port_out":
    #    return gf._port_oc_as_port_out( self )

    # =======================================================================

    #def as_port_in_out( self ) -> "gf.port_in_out":
    #    return gf._port_oc_as_port_in_out( self )

    # =======================================================================

    def as_port_oc( self ) -> "gf.port_oc":
        return self

    # =======================================================================

# ===========================================================================

