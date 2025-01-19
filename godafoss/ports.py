# ===========================================================================
#
# file     : ports.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================
#
# port superclasses (used in type hints)
#
# ===========================================================================

class can_port_in:

    """
    acceptable as :class:`~godafoss.port_in` argument
    """

    pass


# ===========================================================================

class can_port_out:

    """
    acceptable as :class:`~godafoss.port_out` argument
    """

    pass


# ===========================================================================

class can_port_in_out:

    """
    acceptable as :class:`~godafoss.port_in_out` constructor argument
    """

    pass


# ===========================================================================

class can_port_oc:

    """
    acceptable as :class:`~godafoss.port_oc` argument
    """

    pass


# ===========================================================================
#
# basic ports
#
# ===========================================================================

class port_in(
    can_port_in
):

    """
    digital input port

    A port_in is constructed from pins that can function as inputs.

    A port_in can be read as a whole.
    The lowest bit of the value corresponds to the first pin
    of the list of pins passed to the constructor.

    Individual pins can be accessed by indexing the pin attribute.
    """

    # =======================================================================

    def __init__(
        self,
        *args
    ) -> None:
        self.pins = [
            gf.pin_in( pin )
            for pin in gf.make_tuple( *args )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> int:

        """
        the pin values as one int value
        """

        result = 0
        for pin in self.pins[ :: -1 ]:
            result = result << 1
            if pin.read():
                result |= 0b1
        return result

    # =======================================================================

    def as_port_in(
        self
    ) -> "port_in":
        return self

    # =======================================================================

    def inverted(
        self
    ) -> "port_in":
        return _port_in_inverted( self )

    # =======================================================================

    def __neg__(
        self
    ) -> "port_in":
        return _port_in_inverted( self )

    # =======================================================================

    def mirrored(
        self
    ) -> "port_in":
        return _port_in_mirrored( self )

    # =======================================================================


# ===========================================================================

class port_out(
    can_port_out
):

    """
    digital output port

    A port_out is constructed from pins that can function as outputs.

    A port_out can be written as a whole.
    The lowest bit of the value corresponds to the first pin
    of the list of pins passed to the constructor.

    Individual pins can be accessed by indexing the pin attribute.
    """

    # =======================================================================

    def __init__(
        self,
        *args
    ) -> None:

        self.pins = [
            gf.pin_out( pin )
            for pin in gf.make_tuple( *args )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        for pin in self.pins:
            pin.write( ( values & 0b1 ) == 0b1 )
            values = values >> 1

    # =======================================================================

    def inverted(
        self
    ) -> "port_out":
        return _port_out_inverted( self )

    # =======================================================================

    def __neg__(
        self
    ) -> "gf.port_out":
        return _port_out_inverted( self )

    # =======================================================================

    def mirrored(
        self
    ) -> "port_out":
        return _port_out_mirrored( self )

    # =======================================================================

    def as_port_out(
        self
    ) -> "port_out":
        return self

    # =======================================================================

    def as_pin_out(
        self
    ) -> "gf.pin_out":
        return _port_out_as_pin_out( self )

    # =======================================================================


# ===========================================================================

class port_in_out(
    can_port_in,
    can_port_out,
    can_port_in_out,
    can_port_oc
):

    """
    digital push-pull input//output port

    A port_in_out is constructed from pins
    that can function as input//outputs.

    A port_in_out can be read or written as a whole, subject to the
    relevant pins being set to the correct direction:
    call directions_set_input() to prepare all pins
    for a read, or call directions_set_output() to prepare
    all pins for a write.

    The pin value read for a pin that is output is not defined.
    A pin value written to a pin that is input might or might not
    have an effect once the pin is set to output.

    For reading and writing, the lowest bit of the value
    corresponds to the first pin
    of the list of pins passed to the constructor.

    Individual pins can be accessed by indexing the pin attribute.
    """

    # =======================================================================

    def __init__(
        self,
        *args
    ) -> None:
        #print( args )
        #print( gf.make_tuple( args ) )
        self.pins = [
            gf.pin_in_out( pin )
            for pin in gf.make_tuple( *args )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def _directions(
        self
    ) -> int:
        result = 0
        for pin in self.pins:
            result = result << 1
            if pin.direction_is_input():
                result |= 0x01
            print( pin, pin.direction_is_input(), result )
        return result

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:

        """
        set the pin directions according to {directions}
        """

        self.directions = directions
        for pin in self.pins:
            pin.direction_set( directions & 0x01 )
            directions = directions >> 1

    # =======================================================================

    def directions_set_input(
        self
    ) -> None:

        """
        set all pins to input
        """

        self.directions_set( gf.invert_bits( 0, self.number_of_pins ) )

    # =======================================================================

    def directions_set_output(
        self
    ) -> None:

        """
        set all pins to output
        """

        self.directions_set( 0 )

    # =======================================================================

    def read(
        self
    ) -> int:

        """
        the pin values as one int value
        """

        result = 0
        for pin in self.pins[ :: -1 ]:
            result = result << 1
            if pin.read():
                result |= 0b1
        return result

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        for pin in self.pins:
            pin.write( ( values & 0b1 ) == 0b1 )
            values = values >> 1

    # =======================================================================

    def inverted(
        self
    ) -> "port_in_out":
        return _port_in_out_inverted( self )

    # =======================================================================

    def __neg__(
        self
    ) -> "port_in_out":
        return _port_in_out_inverted( self )

    # =======================================================================

    def mirrored(
        self
    ) -> "port_in_out":
        return _port_in_out_mirrored( self )

    # =======================================================================

    def as_port_in(
        self
    ) -> "port_in":
        return _port_in_out_as_port_in( self )

    # =======================================================================

    def as_port_out(
        self
    ) -> "port_out":
        return _port_in_out_as_port_out( self )

    # =======================================================================

    def as_port_in_out(
        self
    ) -> "port_in_out":
        return self

    # =======================================================================

    def as_port_oc(
        self
    ) -> "port_oc":
        return _port_in_out_as_port_oc( self )

    # =======================================================================


# ===========================================================================

class port_oc(
    can_port_in,
    can_port_out,
    can_port_in_out,
    can_port_oc
):
    """
    digital open-collector input//output port

    A port_in_out is constructed from pins
    that can function as open-collector input//outputs.

    A port_oc can be read or written as a whole, subject to the
    relevant pins written high by a previous write.
    The pin value read for a pin that was written low will
    be low.

    For reading and writing, the lowest bit of the value
    corresponds to the first pin
    of the list of pins passed to the constructor.

    Individual pins can be accessed by indexing the pin attribute.
    """

    # =======================================================================

    def __init__(
        self,
        *args
    ) -> None:

        self.pins = [
            gf.pin_in_out( pin )
            for pin in gf.make_tuple( *args )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> int:

        """
        the pin values as one int value
        """

        result = 0
        for pin in self.pins[ :: -1 ]:
            result = result << 1
            if pin.read():
                result |= 0b1
        return result

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        for pin in self.pins:
            pin.write( ( values & 0b1 ) == 0b1 )
            values = values >> 1

    # =======================================================================

    def inverted(
        self
    ) -> "port_in_out":
        return _port_oc_inverted( self )

    # =======================================================================

    def __neg__(
        self
    ) -> "port_in_out":
        return _port_oc_inverted( self )

    # =======================================================================

    def mirrored(
        self
    ) -> "port_in_out":
        return _port_oc_mirrored( self )

    # =======================================================================

    def as_port_in(
        self
    ) -> "port_in":
        return _port_oc_as_port_in( self )

    # =======================================================================

    def as_port_out(
        self
    ) -> "port_out":
        return _port_oc_as_port_out( self )

    # =======================================================================

    def as_port_in_out(
        self
    ) -> "port_in_out":
        return _port_oc_as_port_in_out( self )

    # =======================================================================

    def as_port_oc(
        self
    ) -> "gf.port_oc":
        return self

    # =======================================================================


# ===========================================================================
#
# port proxies
#
# ===========================================================================

class port_in_proxy(
    port_in
):

    """
    base class for a port_in for remote pins

    Acess to proxy pins (like on a GPIO extender) is provided
    by deriving from this class an providing a read() implementation.
    """

    # =======================================================================

    def __init__(
        self,
        nr_of_pins: int
    ) -> None:
        port_in.__init__()
        self.pins = [
            _port_in_pin_proxy( self, n )
            for n in range( number_of_pins )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> None:

        """
        the pin values

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================


# ===========================================================================

class port_out_proxy(
    port_out
):

    """
    base class for a port_out for remote pins

    Acess to proxy pins (like on a GPIO extender) is provided
    by deriving from this class an providing
    read() and write() implementations.
    """

    # =======================================================================

    def __init__(
        self,
        nr_of_pins: int
    ) -> None:
        port_out.__init__()
        self.pins = [
            _port_out_pin_proxy( self, n )
            for n in range( number_of_pins )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:

        """
        write {value} to the pins

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================

# ===========================================================================

class port_in_out_proxy(
    port_in_out
):

    """
    base class for a port_in_out for remote pins

    Acess to proxy pins (like on a GPIO extender) is provided
    by deriving from this class an providing
    set_directions(), read() and write() implementations.
    """

    # =======================================================================

    def __init__(
        self,
        nr_of_pins
    ) -> None:
        port_in_out.__init__()
        self.pins = [
            _port_out_pin_proxy( self, n )
            for n in range( number_of_pins )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:

        """
        set the pin directions according to {directions}

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================

    def read(
        self
    ) -> None:

        """
        the pin values

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:

        """
        write {value} to the pins

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================


# ===========================================================================

class port_oc_proxy(
    port_oc
):

    """
    base class for a port_oc for remote pins

    Acess to proxy pins (like on a GPIO extender) is provided
    by deriving from this class an providing
    read() and write() implementations.
    """

    # =======================================================================

    def __init__(
        self,
        nr_of_pins: int
    ) -> None:
        port_oc.__init__()
        self.pins = [
            _port_oc_pin_proxy( self, n )
            for n in range( number_of_pins )
        ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> None:

        """
        the pin values

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:

        """
        write {value} to the pins

        A subclass must implement this method.
        """

        raise NotImplementedError

    # =======================================================================


# ===========================================================================
#
# pin proxies
#
# used in the implementation of the port proxies
#
# ===========================================================================

def _make_masks(
    myself,
    n: int
):
    myself._mask = 0x01 << n
    myself._inverted_mask = gf.invert_bits(
        myself._mask,
        myself._port.number_of_pins
    )

# ===========================================================================

class _port_in_pin_proxy(
    gf.pin_in
):

    # =======================================================================

    def __init__(
        self,
        port: port_in,
        n: int
    ) -> None:
        self._port = port
        _make_masks( self, n )
        gf.pin_in.__init__( self, None )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return ( self._port.read() & self._mask ) != 0

    # =======================================================================


# ===========================================================================

class _port_out_pin_proxy(
    gf.pin_out
):

    # =======================================================================

    def __init__(
        self,
        port: port_out,
        n: int
    ) -> None:
        self._port = port
        self._port._write_buffer = 0
        _make_masks( self, n )
        gf.pin_out.__init__( self, None )

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        if value:
            self._port._write_buffer |= self._mask
        else:
            self._port._write_buffer &= self._inverted_mask
        self._port.write( self._port._write_buffer )

    # =======================================================================


# ===========================================================================

class port_in_out_pin_proxy(
    gf.pin_in_out
):

    # =======================================================================

    def __init__(
        self,
        port: port_in_out,
        n: int
    ) -> None:
        self._port = port
        self._port._write_buffer = 0
        self._port._directions_buffer = 0
        _make_masks( self, n )
        gf.pin_in_out.__init__( self, None )

    # =======================================================================

    def _direction_set(
        self,
        direction: gf.Union[ bool, int ]
    ) -> None:
        if direction:
            self._port._directions_buffer |= self._mask
        else:
            self._port._directions_buffer &= self._inverted_mask
        print( "directions now %02X" % self._port._directions_buffer )    
        self._port.directions_set( self._port._directions_buffer )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return ( self._port.read() & self._mask ) != 0

    # =======================================================================

    def write(
        self,
        value: gf.Union[ bool, int ]
    ) -> None:
        if value:
            self._port._write_buffer |= self._mask
        else:
            self._port._write_buffer &= self._inverted_mask
        self._port.write( self._port._write_buffer )

    # =======================================================================


# ===========================================================================

class _port_oc_pin_proxy(
    gf.pin_oc
):

    # =======================================================================

    def __init__(
        self,
        port: port_oc,
        n: int
    ) -> None:
        self._port = port
        self._port._write_buffer = 0
        _make_masks( self, n )
        gf.pin_oc.__init__( self, None )

    # =======================================================================

    def read(
        self
    ) -> bool:
        return ( self._port.read() & self._mask ) != 0

    # =======================================================================

    def write(
        self,
        value: gf.Union[ bool, int ]
    ) -> None:
        if value:
            self._port._write_buffer |= self._mask
        else:
            self._port._write_buffer &= self._inverted_mask
        self._port.write( self._port._write_buffer )

    # =======================================================================


# ===========================================================================
#
# type conversions
#
# ===========================================================================

class _port_in_out_as_pin_out(
    gf.pin_out
):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        gf.pin_out.__init__( self )
        self._slave.directions_set_output()

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        self._slave.write( -1 if value else 0 )

    # =======================================================================


# ===========================================================================

class _port_in_out_as_port_in(
    port_in
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_in.__init__( self )
        self.pins = [ pin.as_pin_in() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )


    # =======================================================================

    def read(
        self
    ) -> int:
        return self._slave.read()

    # =======================================================================


# ===========================================================================

class _port_in_out_as_port_out(
    port_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_out.__init__( self )
        self.pins = [ pin.as_pin_out() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write( value )

    # =======================================================================


# ===========================================================================

class _port_in_out_as_port_oc(
    port_oc
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_oc.__init__( self )
        self.pins = [ pin.as_pin_oc() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write( values )
        self._slave.directions_set( values )

    # =======================================================================

    def read(
        self
    ) -> int:
        return self._slave.read()

    # =======================================================================


# ===========================================================================

class _port_oc_as_port_in(
    port_in
):

    # =======================================================================

    def __init__(
        self,
        slave: port_oc
    ) -> None:
        self._slave = slave
        port_in.__init__( self )
        self.pins = [ pin.as_pin_in() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )
        self._slave.write( -1 )

    # =======================================================================

    def read(
        self
    ) -> int:
        return self._slave.read()

    # =======================================================================


# ===========================================================================

class _port_oc_as_port_out(
    port_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_oc
    ) -> None:
        self._slave = slave
        port_in_out.__init__( self )
        self.pins = [ pin.as_pin_out() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write( values )

    # =======================================================================


# ===========================================================================

class _port_oc_as_port_in_out(
    port_in_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_oc
    ) -> None:
        self._slave = slave
        port_in_out.__init__( self )
        self.pins = [ pin.as_pin_in_out() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )
        self._directions_buffer = -1

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self._directions_buffer = directions
        for pin in self.pins:
            pin.direction_set( directions & 0x01 )
            directions = directions >> 1

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write( values or self._directions_buffer )

    # =======================================================================

    def read(
        self
    ) -> int:
        return self._slave.read()

    # =======================================================================


# ===========================================================================
#
# mirror decorators
#
# ===========================================================================

class _port_in_mirrored(
    port_in
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in
    ) -> None:
        self._slave = slave
        port_in.__init__( self )
        self.pins = list( reversed( self._slave.pins ) )
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> int:
        return gf.mirror_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================

class _port_out_mirrored(
    port_out
):

    # =======================================================================

    def __init__(
        self,
        slave
    ) -> None:
        self._slave = slave
        port_out.__init__( self )
        self.pins = list( reversed( self._slave.pins ) )
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write(
            gf.mirror_bits(
                value,
                self.number_of_pins
            )
        )

    # =======================================================================


# ===========================================================================

class _port_in_out_mirrored(
    port_in_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_in_out.__init__( self )
        self.pins = list( reversed( self._slave.pins ) )
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self._slave.directions_set(
            gf.mirror_bits(
                directions,
                self.number_of_pins
            )
        )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write(
            gf.mirror_bits(
                values,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read(
        self
    ) -> int:
        print( "1255", self._slave.read(), self.number_of_pins )
        return gf.mirror_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================

class _port_oc_mirrored(
    port_oc
):

    # =======================================================================

    def __init__(
        self,
        slave: port_oc
    ) -> None:
        self._slave = slave
        port_in_out.__init__( self )
        self.pins = list( reversed( self._slave.pins ) )
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        values: int
    ) -> None:
        self._slave.write(
            gf.mirror_bits(
                values,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read(
        self
    ) -> int:
        return gf.mirror_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================
#
# inversion decorators
#
# ===========================================================================

class _port_in_inverted(
    port_in
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in
    ) -> None:
        self._slave = slave
        port_in.__init__( self )
        self.pins = [ pin.inverted() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def read(
        self
    ) -> int:
        return gf.invert_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================

class _port_out_inverted(
    port_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_out
    ) -> None:
        self._slave = slave
        port_out.__init__( self )
        self.pins = [ pin.inverted() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write(
            gf.invert_bits(
                value,
                self.number_of_pins
            )
        )

    # =======================================================================

# ===========================================================================

class _port_in_out_inverted(
    port_in_out
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_in_out.__init__( self )
        self.pins = [ pin.inverted() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def directions_set(
        self,
        directions: int
    ) -> None:
        self._slave.directions_set( directions )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write(
            gf.invert_bits(
                value,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read(
        self
    ) -> int:
        return gf.invert_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================

class _port_oc_inverted(
    port_oc
):

    # =======================================================================

    def __init__(
        self,
        slave: port_in_out
    ) -> None:
        self._slave = slave
        port_oc.__init__( self )
        self.pins = [ pin.inverted() for pin in self._slave.pins ]
        self.number_of_pins = len( self.pins )

    # =======================================================================

    def write(
        self,
        value: int
    ) -> None:
        self._slave.write(
            gf.invert_bits(
                value,
                self.number_of_pins
            )
        )

    # =======================================================================

    def read(
        self
    ) -> int:
        return gf.invert_bits(
            self._slave.read(),
            self.number_of_pins
        )

    # =======================================================================


# ===========================================================================
#
# tests & demos
#
# ===========================================================================

def port_dummy(
    number_of_pins
) -> port_out:
    result = port_in_out()
    result.number_of_pins = number_of_pins
    return result


# ===========================================================================

def kitt(
    port,
    interval = 50_000,
    iterations = None
) -> None:
    """
    kitt display

    Show the Kitt on the port with the specified interval
    for the specified number of iterations
    (defaults to infinite).

    Times are in us (microseconds).
    """

    p = port.as_port_out()
    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            for n in range( 1 ):
                p.write( 0 )
                gf.sleep_us( 0 )
            gf.report_memory_and_time()

        for n in range( p.number_of_pins ):
            p.write( 0b1 << n )
            gf.sleep_us( interval )

        for n in range( p.number_of_pins - 2, 0, -1 ):
            p.write( 0b1 << n )
            gf.sleep_us( interval )

# ===========================================================================
