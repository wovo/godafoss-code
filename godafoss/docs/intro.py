# ===========================================================================
#
# file     : intro.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

"""
$$insert_image( "godafoss-waterfalls", 700, link="https://wovo.github.io/godafoss" )

This is work in progress
=============================================================================
**The code and the documentation might (or rather, will) be out of sync.**

Name
=============================================================================

The
`Godafoss waterfall <https://en.wikipedia.org/wiki/Go%C3%B0afoss>`_
in northern Iceland is the place where,
according to a (probably fabricated) legend, around the year 1000,
lawspeaker and pagan priest
`Thorgeir Ljosvetningagodi Thorkelsson
<https://en.wikipedia.org/wiki/Thorgeir_Ljosvetningagodi>`_
threw his statues of Norse gods in the water to express
`his support for Christianity
<https://sagamuseum.is/overview/#thorgeir-ljosvetningagodi>`_,
thus avoiding a civil war.

Purpose
=============================================================================

Godafoss is a library for use with
`MicroPython <https://micropython.org>`_,
the Python port for micro-controllers.
It grew out of my frustration that many MicroPython libraries
exist, but don't combine well.
So the obvious solution is
`to create one more <https://xkcd.com/927/>`_, in which I can
throw my MicroPython work.

The godafoss library provides a consistent interface
to the hardware of the target chip or
module itself, and to various peripheral chips and modules.
The emphasis is on ease of use, portability and abstraction,
rather than ultimate speed or providing all features of all peripherals.

Installation
=============================================================================

**Built into a MicroPython Image**

The preferred option is to use a MicroPython image with the library built in.
This is easy, and yields the shortest startup time and the lowest RAM use.
Images for selected targets are available,
built from recent (1.22) MicroPython sources:
`rp2040 <./images/rp2040-gf.uf2>`_,
`rp2040w <./images/rp2040w-gf.uf2>`_ (with WiFi),
`esp8266 <./images/esp8266-gf.bin>`_,
`esp32 <./images/esp32-gf.bin>`_ (dual core LX7),
`esp32s2 <./images/esp32s2-gf.bin>`_ (single core LX7),
`esp32s3 <./images/esp32s3-gf.bin>`_ (dual core LX7),
`esp32c2 <./images/esp32c2-gf.bin>`_ (single core RISC-V),
`esp32c3 <./images/esp32c3-gf.bin>`_ (dual core RISC-V),
`teensy 4.0 <./images/teensy40-gf.hex>`_,
`teensy 4.1 <./images/teensy41-gf.hex>`_
.

**Compiled**

Alternatively, the compiled form of the library (.mpy files)
can be installed using
`mpremote <https://docs.micropython.org/en/latest/reference/mpremote.html>`_
on the host
(PC/laptop) command line (my MicroPython devices are always on com42)::

    mpremote connect com42 mip install github:wovo/godafoss

Or if you prefer to install the .mpy files manually:

    - clone http://www.github.com/wovo/godafoss
    - copy the godafoss directory to the target MicroPython device,
      for instance using the file upload function in Thonny

**As sources**

Finally, to use the library in its source form
(for debugging or extending the library):

    - clone the
      Godafoss code repository http://www.github.com/wovo/godafoss-code
    - copy the godafoss directory to the target MicroPython device

For working on the library sources
a fast target with ample RAM is recommended.
My current (2024) preference is the Teensy 4.1
(a pity its MicroPython port doesn't have the nexopixel driver built in).


Blinky
=============================================================================

Once installed, godafoss can be used by importing it.
For the blinky below,
replace 25 with the number or other identification of the gpio pin
that connects to the LED on your target::

    # PiPico has a led on GPIO 25
    import godafoss as g$-$f
    g$-$f.blink( 25 )

Boards
-----------------------------------------------------------------------------
The library supports generic MicroPython,
but it also has explicit support
for the following boards and modules.

$$insert_table( "boards", 3 )


Displays
-----------------------------------------------------------------------------
The library provides drivers for various (LCD, OLED and E-ink) display
controllers. These controllers often need parameters that
depend on the particular display.
For the following displays drivers are provided that
are taylored with those parameters.

$$insert_table( "displays", 4 )

Abstract data types
-----------------------------------------------------------------------------

The library uses abstractions for things like color, temperature,
relative amount, and coordinates.
These immutable abstract data classes are
:class:`~godafoss.color`,
:class:`~godafoss.temperature`,
:class:`~godafoss.fraction`,
:class:`~godafoss.xy`, and
:class:`~godafoss.xyz`.
When appropriate, objects of these classes support arithmetic operations
like addition, subtraction, multiplication and division.


Pins
-----------------------------------------------------------------------------

The library uses four types of pins: input, output, input_output,
and open collector.
An input pin has only a read() method, and output pin only a write() method.
An input_output pin and an open_collector pin have
both read() and write() methods.
An input_output pin also has methods to set the direction
to input or output.

+----------------------------+----------+----------+-------------------------+
| class                      | read()   | write()  | direction_set_input()   |
|                            |          |          | direction_set_output()  |
+----------------------------+----------+----------+-------------------------+
| :class:`~pin_in`           |    x     |          |                         |
+----------------------------+----------+----------+-------------------------+
| :class:`~pin_out`          |          |    x     |                         |
+----------------------------+----------+----------+-------------------------+
| :class:`~pin_in_out`       |    x     |    x     |     x                   |
+----------------------------+----------+----------+-------------------------+
| :class:`~pin_oc`           |    x     |    x     |                         |
+----------------------------+----------+----------+-------------------------+

For an input_output pin, the appropriate direction_set method must be
called before a read() or write() method is called.
For an open_collector pin a low (zero, False) value written to the pin
is dominant, so a read() is meaningfull only after a high value (1, True) has
been written to the pin.

The pin class constructors accept either a board pin number or string,
None, or a pin object that can be used in the requested way:

    - a :class:`~godafoss.pin_in` can be used to construct a
      :class:`~godafoss.pin_in` (of course)
    - a :class:`~godafoss.pin_out` can be used to construct a
      :class:`~godafoss.pin_out` (of course)
    - a :class:`~godafoss.pin_in_out` can be used to construct
      :class:`~godafoss.pin_in_out` (of course), but
      also to construct a :class:`~godafoss.pin_in`,
      a :class:`~godafoss.pin_out`,
      or a :class:`~godafoss.pin_oc`
    - a :class:`~godafoss.pin_oc` can be used to construct a
      :class:`~godafoss.pin_oc` (of course), but
      also to construct a :class:`~godafoss.pin_in`,
      a :class:`~godafoss.pin_out`,
      or a :class:`~godafoss.pin_in_out`
      (but the as :class:`~godafoss.pin_in_out` or
      :class:`~godafoss.pin_out` it will let the pin float instead
      of driving it high).

When initialized with an integer or string,
the board-specific pin support built into micro-python
is used to create the pin.
In this case, the constructor will accept pullup an/or pulldown
parameters can be set to True to activate the pullup or pulldown
functionality of the pin.

When called with None, a dummy object of the appropriate type is returned.

Two pins that have a write() method can be added (+ operator) to create a
$$ref( "pin_out" )
that writes to both pins.

Ports
-----------------------------------------------------------------------------

GPIO pins and ports (ports are ordered groups of pins)
are subclasses of the pin superclasses
:class:`~godafoss.pin_in`,
:class:`~godafoss.pin_out`,
:class:`~godafoss.pin_in_out`, and
:class:`~godafoss.pin_oc`,
and the port superclasses
:class:`~godafoss.port_in`,
:class:`~godafoss.port_out`,
:class:`~godafoss.port_in_out`, and
:class:`~godafoss.port_oc`.

Ports and pins have read() and write() methods
(when appropriate, a pin_in obviously doesn't have a write() method),
pin_in_out and port_in_out additionally
have direction_set(), direction_set_input(), and direction_set_output()
methods.

Whenever appropriate, a pin or port has
as_pin_in(), as_pin_out(), as_pin_in_out(), as_pin_oc()
(or as_port_in() etc.) methods,
which return an object that accesses the same pin or port,
but behaves as the requested pin or port type.

A function that needs for instance a pin_out,
should accept any parameter value that can be
converted to a pin_out by calling make_pin_out() internally.
The blink demo for instance, can be called
with a number, a string (required on the Pi Pico W),
a pin_out, pin_in_out, or a pin_oc::

    import godafoss as gf
    gf.blink( 42 ) # PiPico
    gf.blink( "LED" )  # PiPico W
    gf.blink( gf.make_pin_out( 42 ) ) # some esp32 boards

A pin is an example of an object that is
:class:`~godafoss.invertible`:
you can use a minus operator, the invertrt modifier, or
the .inverted() method to get a pin that has the opposite
behaviour for of its read() and write() methods:
when the original pin would read True, the inverted pin
reads False, etc.


Displays
-----------------------------------------------------------------------------

frame?

A display is something that can show things
at locations in a rectangular grid.
A display has a size, a flush function and a draw function.
The draw function takes an xy coordinate, and draws something
at the location specified by that coordinate.
There are three different types of displays, which
differ in what can be drawn ate each location:

    - on a canvas, a each location is a color pixel
    - on a sheet, each location is a pixel that can be on or off
    - on a terminal, each location is an (ASCII) character

Most displays are buffered


Terminal
-----------------------------------------------------------------------------

The
:class:`~godafoss.terminal`
class abstracts a rectangular area of characters.
The interface of a terminal are its clear(), cursor_set() and write() methods.
The classic example of a terminal is an
:class:`~godafoss.hd44780`
character lcd,
but a terminal can also be constructed from a graphic
:class:`~godafoss.canvas`
and a
:class:`~godafoss.font`.


Graphics
-----------------------------------------------------------------------------


image tool
font tool


Resource use
-----------------------------------------------------------------------------

On most MicroPython targets, RAM is a scarce.
To make the most of the available RAM the library uses on-demand loading:
most things within the library, and most attributes of its classes,
are loaded only when used.
This saves overall RAM, but at the cost of some overhead in loading time
and RAM for administration of the things that are actually loaded .

The next table shows the total target RAM,
the amount of RAM available for a MicroPython application,
the RAM left when Godafoss core is loaded,
and the time it takes to load the Godafosss core.
This is for the host-compiled version (.mpy files), loading
the source version takes around 10 times more time.)

+--------------+------------+-----------------+----------------+---------------+
| Target       | Target RAM | MicroPython RAM | Godafoss core  | Godafoss full |
+--------------+------------+-----------------+----------------+---------------+
| ESP8266      |     80 Kb  |      33 Kb      | 12 Kb, 300 ms  |      -        |
+--------------+------------+-----------------+----------------+---------------+
| ESP32        |    320 Kb  |     106 Kb      |     60 Kb      |     40 Kb     |
+--------------+------------+-----------------+----------------+---------------+
| ESP32 psiram |      8 Mb  |       4 Mb      |                |               |
+--------------+------------+-----------------+----------------+---------------+
| ESP32-C3     |    400 Kb  |     122 Kb      |                |               |
+--------------+------------+-----------------+----------------+---------------+
| Pi Pico      |    264 Kb  |    185 Kb       |                |               |
+--------------+------------+-----------------+----------------+---------------+
| Pi Pico W    |    264 Kb  |    159 Kb       |                |               |
+--------------+------------+-----------------+----------------+---------------+
| Teensy 4.1   |      1 Mb  |    744 Kb       |                |               |
+--------------+------------+-----------------+----------------+---------------+
| Nano 33 BLE  |    256 Kb  |       ?         |                |               |
+--------------+------------+-----------------+----------------+---------------+

The ESP8266 and Micro:bit can run MicroPython, but the amount of RAM
on these platforms is too small to use Godafoss.

Most modern 'micro-controllers' use an external Flash chip to store
the application code (in this case the MicroPython system),
but load it into RAM for execution.
This explains the large gap between the total target RAM,
and the amount of RAM available for use inside MicroPython.
For a Pi Pico W the gap is larger than for a plain Pi Pico,
because the W version supports the extra features of the WiFi module.

The ESP8266 is different: it uses its limited RAM (partically)
to cache the application code, hence the gap between total target RAM and
MicroPython RAM is much smaller than for the other targets.

The ESP32 psiram target uses an external SPI RAM chip,
using its internal RAM as a cache.
This setup provides ample RAM,
at the expense of (some) performance.
Currently only up to 4 Mb of the RAM chip seems to be used.


License
-----------------------------------------------------------------------------

The library is covered by the MIT license,
so you can do with it what you want,
except changing the license of the library itself,
or sueing me when it doesn't work as expected.
The MIT license is NOT tainting, so code that uses the
library (your application) is not affected.
The MIT copyright and license text is part of the library
(gf.license),
so you application automatically includes the text, satisfying
the MIT license requirement to include the copyright and license text.


Code structure & conventions
-----------------------------------------------------------------------------

The library code conforms to PEP8 and pylint, except when I disagree
with their rules. Check test/native/_tools.py for details.

My personal language-independent naming convention is snake_case,
so that is what the library uses.

The library uses type hints, even though MicroPython doesn't
support this feature (yet).
The native tests check the hints, and they are used in the documentation.
The type hints and docstring documentation for parameters that can be of
a set of types types use | to separate the alternatives.

In the docstrings
    - macros are used to create a single truth for
      for instance the effect of class being immutable.
    - godafoss types are always references

The library uses microseconds for delays and time durations.
Nanoseconds are a bit fast for a Python interpreter,
and floats add overhead on chips that don't have floating point hardware,
so this seems the best choice.
Please use _ as 1000's separator to make your literals more readable:
a second is 1_000_000 microseconds.

For distance, mm are used.
For temperatures K, C an F are supported by the
:class:`~godafoss.temperature` class.

Whenever reasonably possible,
the library avoids the use of floating point arithmetic.


Library content
-----------------------------------------------------------------------------

"""

# must be present to make loading possible
# must be after the text to prevent the text being sorted by sphinx
intro = None
