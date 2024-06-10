# ===========================================================================
#
# file     : pin_oc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class pin_oc(
    gf.autoloading,
    gf.can_pin_oc,
    gf.can_pin_in,
    gf.can_pin_out,
    gf.can_pin_in_out,
):
    """
    $$see_also( "#pins", "pin_in", "pin_out", "pin_oc", "port_oc" )

    open-collector (or more likely, open-drain) input output pin

    :param pin: (int | str | gf.can_pin_oc | None )
        Either a (int or str) gpio pin indentification,
        or a pin that has an as_pin_oc method()
        (
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
        pin: "int | str | None | gf.can_pin_oc"
    ):

        gf.autoloading.__init__( self, pin_oc )

        if pin is not None:

            try:
                self.worker = pin.as_pin_oc()

            except:
                self.pin_nr = pin
                self.worker = gf.gpio_oc( self.pin_nr )

            # to speed things up: use the workers methods directly
            self.write = self.worker.write
            self.read = self.worker.read

    # =======================================================================

    def read( self ) -> bool:
        """
        return the level on the pin

        :result: (bool)
            the level read from the pin

        When a 0 has been written to the pin, a 0 will be read unless
        there is some serious hardware trouble.
        When a 1 has been written, the level on the pin will be read.
        return self.value
        """

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin output level

        :param value: (bool)
            the level to output to the pin

        When False is written,
        the pin hardware will pull the output level low.
        When True is written,
        the pin hardware will let the pin level float.
        """

        self.value = bool( value )

    # =======================================================================

    def __add__( self, other ) -> "pin_out":
         return gf.pin_out_from_two_pins( self, other )

    # =======================================================================

    def as_pin_oc( self ) -> "pin_oc":
        return self

    # =======================================================================

# ===========================================================================
