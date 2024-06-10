# ===========================================================================
#
# file     : pin_in.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in(
    gf.autoloading,
    gf.can_pin_in
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_in" )

    digital input pin: an object from which you can
    read() a bool value.

    :param pin: (int | str | gf.can_pin_in | None )
        Either a (int or str) gpio pin indentification,
        or a pin that has an as_pin_in method()
        (
        $$ref( "pin_out" )
        ,
        $$ref( "pin_in_out" )
        or
        $$ref( "pin_oc" )
        ),
        or None (return a dummy pin).

    $$methods()
    """

    # =======================================================================

    def __init__(
        self,
        pin: "int | str | None | gf.can_pin_in"
    ):

        gf.autoloading.__init__( self, pin_in )

        if pin is not None:

            try:
                self.worker = pin.as_pin_in()

            except:
                self.pin_nr = pin
                self.worker = gf.gpio_out( self.pin_nr )

            # to speed things up: use the workers method directly
            self.read = self.worker.read

    # =======================================================================

    def read( self ) -> bool:
        """
        return the level on the pin

        :result: (bool)
            the level read from the pin
        """

        return self.value

    # =======================================================================

    def as_pin_in( self ) -> "pin_in":
        "the pin itself"

        return self

    # =======================================================================

# ===========================================================================
