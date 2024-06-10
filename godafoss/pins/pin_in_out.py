# ===========================================================================
#
# file     : pin_in_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_in_out(
    gf.autoloading,
    gf.can_pin_in,
    gf.can_pin_out,
    gf.can_pin_in_out,
    gf.can_pin_oc
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_in_out" )

    digital input output pin

    :param pin: (int | str | gf.can_pin_in_out | None )
        Either a (int or str) gpio pin indentification,
        or a pin that has an as_pin_in_out method()
        (
        $$ref( "pin_in_out" )
        or
        $$ref( "pin_oc" )
        ),
        or None (return a dummy pin).

    When the direction has been set to output,
    a write() determines the pin level.
    When the direction has been set to input,
    a read() returns the pin level.

    Two pins that each have an as_pin_out() method can be added
    (+ operator) to yield a
    $$ref( "port_in_out" )
    that writes to both pins.

    $$methods()
    """

    # =======================================================================

    def __init__(
        self,
        pin: "int | str | None | gf.can_pin_in_out"
    ):

        gf.autoloading.__init__( self, pin_in_out )

        if pin is not None:

            try:
                self.worker = pin.as_pin_in_out()

            except:
                self.pin_nr = pin
                self.worker = gf.gpio_in_out( self.pin_nr )

            # to speed things up: use the workers methods directly
            self.direction_set_input = self.worker.direction_set_input
            self.direction_set_output = self.worker.direction_set_output
            self.write = self.worker.write
            self.read = self.worker.read

    # =======================================================================

    def direction_set_output( self ) -> None:
        "set the pin direction to output"

        self.is_output = True

    # =======================================================================

    def direction_set_input( self ) -> None:
        "set the pin direction to input"

        self.is_output = False

    # =======================================================================

    def read( self ) -> bool:
        """
        when the pin direction has been set to input:
        return the level on the pin

        :result: (bool)
            the level read from the pin
        """
        return self.value

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        when the pin direction has been set to output:
        set the pin output level

        :param value: (bool)
            the level to output to the pin
        """

        self.value = bool( value )

    # =======================================================================

    def as_pin_in_out( self ) -> "pin_in_out":
        "the pin itself"

        return self

    # =======================================================================

    def __add__(
        self,
        other
    ) -> "pin_out":

        return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

# ===========================================================================
