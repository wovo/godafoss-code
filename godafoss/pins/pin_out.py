# ===========================================================================
#
# file     : pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_out(
    gf.autoloading,
    gf.can_pin_out
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_out" )

    digital output pin:
    an object to which you can write() a digital level.

    :param pin: (int | str | gf.can_pin_out | None )
        Either a (int or str) gpio pin indentification,
        or a pin that has an as_pin_in_out method()
        (
        $$ref( "pin_out" )
        ,
        $$ref( "pin_in_out" )
        or
        $$ref( "pin_oc" )
        ),
        or None (return a dummy pin).

    Two pins that each have an as_pin_out() method can be added
    (+ operator) to yield a
    $$ref( "port_in_out" )
    that writes to both pins.

    $$methods()
    """

    # =======================================================================

    def __init__(
        self,
        pin: "int | str | None | gf.can_pin_out"
    ):

        gf.autoloading.__init__( self, pin_out )

        if pin is not None:

            try:
                self.worker = pin.as_pin_out()

            except:
                self.pin_nr = pin
                self.worker = gf.gpio_out( self.pin_nr )

            # to speed things up: use the workers method directly
            self.write = self.worker.write

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin output level

        :param value: (bool)
            the level to output to the pin
        """

        self.value = bool( value )

    # =======================================================================

    def as_pin_out( self ) -> "pin_out":
        "the pin itself"

        return self

    # =======================================================================

    def __add__( self, other ) -> "pin_out":

         return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

# ===========================================================================
