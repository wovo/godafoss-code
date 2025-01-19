# ===========================================================================
#
# file     : basics.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (godafoss.license)
#
# ===========================================================================

# no imports required


# ===========================================================================
#
# take care of the differences between MicroPython and CPython
#
# ===========================================================================

try:
    from micropython import const

    # micropython (embedded)
    running_micropython = True

    _separator = "/"

    import time
    initial_time = time.ticks_us()

    import gc
    gc.collect()
    initial_mem_free = gc.mem_free()

    Any = None
    Type = None
    Optional = None
    Union = None
    Callable = None
    List = None
    Dict = None
    IO = None


except:

    # cpyton (hosted)
    running_micropython = False

    def const( x: any ): return x

    import os
    _separator = os.sep

    uint = None

    import time
    initial_time = time.monotonic_ns() // 1000

    from typing import Any
    from typing import Type
    from typing import Optional
    from typing import Union
    from typing import Callable
    from typing import List
    from typing import Dict
    from typing import IO


# ===========================================================================

class spi_implementation:
    "selects a spi implementation"

    soft = const ( 20 )
    "spi implemented in code (inside MicroPython)"

    hard = const ( 21 )
    "spi implemented by the target hardware"


# ===========================================================================

class orientation:
    north  = const ( 10 )
    east   = const ( 11 )
    south  = const ( 12 )
    west   = const ( 13 )


# ===========================================================================
#
# math utilities
#
# ===========================================================================

def sign(
    x: Union[ int, float ]
) -> int:

    """
    sign (-1, 0, 1 ) of {x}

    :param x: (int, float)
        the value to take the sign of

    :result: (int)
        -1, 0, or 1 respectively for {x} < 0, {x} == 0, or {x} > 0
    """

    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# ===========================================================================

def less(
    x: Union[ int, float ],
    n: Union[ int, float ] = 1
) -> Any:

    """
    step the {x} value {n} towards 0

    :param x: (int, float)
       the start value

    :param n: (int, float)
       the step value (default 1 )

    :result: (int, float)
       x - n for x > 0, x + n for x < 0 (but clamped at 0)


    This function returns the value {x}, plus {n} in the direction of 0.
    When this would pass 0, 0 is returned instead.
    """

    if x > 0:
        return max( 0, x - n )

    else:
        return min( 0, x + n )


# ===========================================================================

def more(
    x: Union[ int, float ],
    n: Union[ int, float ] = 1
) -> Any:

    """
    step the {x} value {n} away from 0 0

    :param x: (int, float)
       the start value

    :param n: (int, float)
       the step value (default 1 )

    :result: (int, float)
       x + n for x >= 0, x - n for x < 0

    This function returns the value {x}, plus {n} in the direction
    away from 0.
    """

    if x >= 0:
        return x + n

    else:
        return x - n


# ===========================================================================

def within(
    x: Any,
    a: Any,
    b: Any
) -> bool:

    """
    test whether {x} value is between {a} and {b}

    :param x: (Any)
        the value to be checked

    :param a: (Any)
        one bound to check the value against

    :param b: (Any)
        other bound to check the value against

    :result: (bool)
        whether {x} is in the range [a..b] or [b..a]

    This function returns whether {x} is between {a} and {b}.
    The {a} and {b} values are included in the allowed range.
    The {a} and {b} values don't have to be in order.

    examples::
    $insert_example( "test_tools.py", "within example", 1 )
    """

    if a < b:
        return a <= x <= b
    else:
        return b <= x <= a


# ===========================================================================

def clamp(
    x: Any,
    a: Any,
    b: Any
) -> Any:

    """
    {x}, clamped to the nearest value in the range [{a}..{b}]

    :param x: (Any)
        the value to clamp within the range [{a}..{b}]

    :param a: (Any)
        one bound of the clamp interval

    :param b: (Any)
        other bound of the clamp interval

    :result: (Any)
        either {x}, or the nearest value in the range [{a}..{b}]

    The {a} and {b} values don't have to be in order.

    examples
    $insert_example( "test_tools.py", "clamp example", 1 )
    """

    if a < b:
        return max( a, min( x, b ) )
    else:
        return max( b, min( x, a ) )


# ===========================================================================
#
# bit manipulation
#
# ===========================================================================

def bar_bits(
    n_bits: int
) -> int:

    """
    unsigned int value with (only) the lower {n_bits} bits 1

    :param n_bits: int
        the number of 1-value bits in the result

    :result: int
        unsigned int value, with (only) the lower {n_bits} bits 1

    This function returns the integer value,
    of which the lowest {n_ones} bits
    are 1 (set), the other (higher) bits are 0 (clear).

    examples
    $insert_example( "test_tools.py", "bar_bits example", 1 )
    """

    return ( 2 ** n_bits ) - 1


# ===========================================================================

def invert_bits(
    value: int,
    n_bits: int
) -> int:

    """
    the {value}, with its lower {n_bits} bits inverted

    :param value: int
        the value to invert

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the {value}, with its lower {n_bits} bits inverted

    This function returns the {value},
    of which {n_bits} are relevant, with those bits inverted.
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "invert_bits example", 1 )
    """

    return ( ~ value ) & ( ( 0b1 << n_bits ) - 1 )


# ===========================================================================

def mirror_bits(
    value: int,
    n_bits: int
) -> int:

    """
    the {value}, with its lower {n_bits} bits mirrored

    :param value: int
        the value to mirror

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the {value}, with its lower {n_bits} bits mirrored

    This function returns the value, of which n_bits are relevant,
    with the bits mirrored (most significant bit becomse the least
    signififacnt bit and vice verse, etc.)
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "mirror_bits example", 1 )
    """

    result = 0
    for _ in range( n_bits ):
        result = ( result << 1 ) | ( value & 0b01 )
        value = value >> 1
    return result


# ===========================================================================
#
# bytes <-> int conversion
#
# ===========================================================================

def bytes_from_int(
    value: int,
    n_bytes: int
) -> bytes:

    """
    bytes lsb-first representation of an int

    :param value: int
        the value to be converted to bytes

    :param n_bytes: int
        the desired number of bytes

    :result: bytes
        the bytes representation of the value

    This function returns the int value as n_byte bytes,
    least significant byte first (little endian).

    examples
    $insert_example( "test_tools.py", "bytes_from_int example", 1 )
    """

    array = bytearray( n_bytes )
    for i in range( 0, n_bytes ):
        array[ i ] = value & 0xFF
        value = value >> 8
    return bytes( array )


# ===========================================================================

def int_from_bytes(
    array: Union[ bytes, bytearray ],
    signed: bool = False
) -> int:

    """int value from a lowest-byte-first sequence of bytes

    :param array: bytes | bytearray
        the array of bytes that is to be converted to an integer

    :param signed: bool
        treat the resulting bit pattern as unsigned (False, default)
        or signed (True)

    :result: int
        the array interpreted as integer value

    This function returns the bytes as an unsigned integer value,
    the first byte as least significant byte of the int value.

    Python has the int.from_bytes function, but it is currently
    not implemented fully and correctly in MicroPython.
    Hence this alternative.

    examples
    $insert_example( "test_tools.py", "int_from_bytes example", 1 )
    """

    result = 0
    for i in range( len( array ) - 1, -1, -1 ):
        result = ( result << 8 ) | ( array[ i ] & 0xFF )

    if signed and ( ( array[ -1 ] & 0x80 ) != 0 ):
        result = - ( ( result - 1 ) ^ bar_bits( 8 * len( array ) ) )

    return result


# ===========================================================================
#
# object construction
#
# ===========================================================================

def store_arguments(
    target: Any,
    **kwargs
) -> None:

    """
    store the keyword arguments as attributes

    :param target: (Any)
        the object in which the {kwargs} are stored as attributes

    :param **kwargs:
        the name-value pairs that are to be stored in the {target}


    This function stores its {kwargs} as attributes of the {target}.
    The typical use is in an __init__().
    """

    for name, value in kwargs.items():
        target.__setattr__( name, value )


# ===========================================================================

class immutable:

    """
    immutable object

    Python names are references, and class objects are mutable,
    so a class member variable can inadvertently be modified.
    The xy class is immutable, but if it were not, this would
    be possible::

        origin = xy( 0, 0 )
        a = origin
        a.x = 10 # this modifies the object that origin references!
        print( origin.x ) # prints 10

    To prevent such modifications, a value class inherits from freeze,
    and calls immutable._init__( self ) when all its members
    have been initialized.

    usage example
    $insert_example( "test_tools.py", "immutable example", 1 )
    """

    _frozen = False

    # =======================================================================

    def __init__( self ) -> None:
        # after the initialization, the object members can't be modified
        self._frozen = True

    # =======================================================================

    def __delattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__delattr__( self, *args, **kwargs )

    # =======================================================================

    def __setattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__setattr__( self, *args, **kwargs )

    # =======================================================================


# ===========================================================================

class no_new_attributes:

    """
    make it impossible to add new attributes

    In an object that inherits from this class can (after the
    no_new_attributes.__init__() call) no new attributes can be created.
    This can be usefull to prevent accidentally setting an
    attributeb that is spelled wrong.
    """

    _no_new = False

    # =======================================================================

    def __init__( self ) -> None:
        # after the initialization, no new attributes can be created
        self._no_new = True

    # =======================================================================

    def __setattr__( self, name, value ):
        if self._no_new:
            _ = eval( f"self.{name}" )
        object.__setattr__( self, name, value )

    # =======================================================================


# ===========================================================================

class _autoloading:

    """
    load a class method (only) when it is called

    :param class_type: (type)
        the class that inherits from autoloading

    Inheriting from this class puts a mechanism in place that,
    when an attribute is requested that is not present,
    will attempt to import that attribute from the
    <class name>__<attribute name>.py file.

    This is done to decrease startup time and lower RAM use.

    The loaded attribute is added to the class, so on subsequent use
    it will be used directly.
    """

    # =======================================================================

    def __init__(
        self,
        class_type: type
    ):
        self._class_type = class_type
        self._class_name = class_type.__name__

    # =======================================================================

    def __getattr__(
        self,
        obj: str,
        obj_type: [ type or None ] = None
    ):

        if show_loading:
            print( f"load attribute {self._class_name}.{obj}" )

        import gc; gc.collect()

        name = f"{self._class_name}__{obj}"

        try:
            print( f"from godafoss.gf.{name} import {name}" )
            exec( f"from godafoss.gf.{name} import {name}" )

        except:

            # Get the import path for the missing attribute.
            found = _import_path( _path, name )

            if found is None:
                raise AttributeError(
                    f"unknown attribute '{self._class_name}.{obj}'"
                ) from None

            # Import and retrieve the missing attribute
            exec( f"from {found} import {name}" )

        func = constructor = eval( f"{name}" )

        # if it is a class, wrap its constructor in a fuction
        if isinstance( func, type ):
            func = lambda *args, **kwargs: constructor( *args, **kwargs )

        # inject it into the class (not into the object!).
        setattr( self._class_type, obj, func )

        # Return a trampoline that prepends the self argument.
        # This is only relevant for this one call,
        # next time the original function will be found in the class.
        return lambda *args, **kwargs: func( self, *args, **kwargs )

    # =======================================================================


# ===========================================================================
#
# development help
#
# ===========================================================================

def report_memory_and_time():

    """
    report memory and time used since godafoss loading started
    """

    ms = ( time_us() - initial_time ) // 1000

    try:
        import gc
        gc.collect()
        free = gc.mem_free()
        b = gf.initial_free - free
        s = f", memory {b} bytes ({gf.initial_free}->{free})"
    except:
        s = ""

    print( f"time {ms} ms{s}" )


# ===========================================================================

def benchmark( function, *args, **kwargs ):
    """
    decorator for benchmarking

    This function decorator will report the time spent (in microseconds)
    and memory claimed (in bytes) each time the decorated function runs.
    """

    # inspired by similar code on the micropython website

    function_name = str( f ).split( ' ' )[ 1 ]

    # local to avoid loading these modules
    # when this decorator is not used
    from godafoss.gf_gc import collect, mem_free
    from godafoss.gf_time import ticks_us

    def new_function( *args, **kwargs ):

        collect()
        before_bytes = mem_free()
        before_us = ticks_us()

        result = f( *args, **kwargs )

        after_us = ticks_us()
        collect()
        after_bytes = mem_free()

        print( "%s took %d us, claimed %d bytes" % (
            function_name,
            after_us - before_us,
            before_bytes - after_bytes
        ) )

        return result

    return new_function


# ===========================================================================

def print_info():
    """
    print the target name and some memory information

    This function is meant to give a quick impression of your target system.

    You can cut-n-paste the function body to use it without Godafoss.
    """

    # The includes are local so you can cut-n-paste the function body
    # to use it outside godafoss, for instance to explore a new target

    import gc, os, micropython

    gc.collect()
    print( "Name           %8s"  % ( "'" + os.uname()[ 0 ] ) + "'" )
    print( "RAM allocated %8d B" % gc.mem_alloc() )
    print( "RAM free      %8d B" % gc.mem_free() )

    try:
        s = os.statvfs( "//" )
        print( "FLASH free    %8d B" % ( s[ 0 ] * s[ 3 ] ) )
    except:
        print( "target has no os.statvfs()" )

    print( "mem info:" )
    micropython.mem_info()


# ===========================================================================
#
#
#
# ===========================================================================

def all( first, *args ):
    return first.combine( *args )


# ===========================================================================

def make_tuple(
    *args: any
) -> any:
    """
    make a tuple from a tuple or list, or from a number of arguments

    :param \*args: any
        the arguments are to be turned into a tuple

    :result: any
        a tuple constructed from the \*args

    When called with one argument, which is a list or a tuple,
    this function returns it as a tuple.
    Otherwise, it returns a tuple of its argument(s).

    examples::
    $insert_example( "test_tools.py", "make_tuple example", 1 )
    """

    if len( args ) == 1 and isinstance( args[ 0 ], ( list, tuple ) ):
        return tuple( args[ 0 ] )
    else:
        return tuple( args )


# ===========================================================================

class repeater:
    """
    iterate the indicated number of iterations, or forever when None

    :param iterations: int | None
        the number of iterations, or None for infinite iterationfs

    This iterator is usefull for iterative demos that by default
    must run forever, but might be used to run a fixed numer of times.

    The first iterator value is 0, the next is 1.
    When a number of iterations is specified, the value increments,
    otherwise it remains 1.

    examples::

        for _ in repeater( 10 ): ...  # ... is repeated 10 times
        for _ in repeater( None ): ...  # ... is repeated forever
    """

    # =======================================================================

    def __init__(
        self,
        iterations: int | None
    ) -> None:
        self.iterations = iterations
        self.n = None

    # =======================================================================

    def __iter__( self ):
        self.n = -1
        return self

    # =======================================================================

    def __next__( self ):
        if self.iterations is not None:
            self.n += 1
            if self.n >= self.iterations:
                raise StopIteration
        else:
            self.n = min( 1, self.n + 1 )
        return self.n

    # =======================================================================


# ===========================================================================

class remember:
    """
    """

    def __init__( self, addresses ):
        self._addresses = [ address for address in addresses ]
        self._data = [ machine.mem32[ address ] for address in addresses ]

    def restore( self ):
        for address, data in zip( self._addresses, self._data ):
            machine.mem32[ address ] = data

# ===========================================================================

def time_us() -> int:
    if running_micropython:
        return time.ticks_us()
    else:
        return time.monotonic_ns() // 1000


# ===========================================================================

def elapsed_us( f, *args, **kwargs ):
    """
    time a function call

    This function calls the function f with the provided parameters
    and returns the elapsed time in microseconds
    """

    before = gf.ticks_us()
    f( *args, *kwargs )
    after = gf.ticks_us()
    return after - before


# ===========================================================================

def sleep_us( t: int ) -> None:
    if running_micropython:
        time.sleep_us( t )
    else:
        time.sleep( t / 1_000_000 )

# ===========================================================================
