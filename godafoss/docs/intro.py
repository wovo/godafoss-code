# ===========================================================================
#
# file     : intro.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

"""
$insert_image( "godafoss-waterfalls", 0, 600 )

Purpose
-------

Godafossis a library for use with MicroPython.
It provides a consistent interface to the hardware of the target chip or
module itself, and to various peripheral chips and modules.
The emphasis is on portability and abstraction,
rather than speed or providing all features of all peripherals.

Name
-------
The Godafoss fall in northern Iceland is the place where, according to a
(probably fabricated) legend, lawspeaker and former pagan priest Thorgeir
Ljosvetningagodi threw his statues of Norse gods in the water to express
his support for Christianity, thus avoiding a civil war.


Use
---
If you want to use the library (as opposed to tinker with the library code)
the preferred option is to use an image with the lbrary built in as
frozen code. This yields the shortest startup time and the lowest RAM use.
Images for a few targets are available, built from the latest MicroPython:
version (1.22): 
rp2040 (Raspberry Pi Pico),
rp2040w (Raspberry Pi Pico with WiFi),
esp32,
esp32s2 (single CPU),
esp32c3 (RISC V),
Teensy $.1
.

The library can be installed by using mpremote from the host 
(PC/laptop) command line
(my MicroPython devices are always on com42)::

    python -m mpremote connect com42 mip install github:wovo/godafoss

Or if you prefer to install the manually:

    - clone http://www.github.com/wovo/godafoss
    - copy the lib directory to the target MicroPython device,
      for instance using the file download funtion in Thonny

To use the library in its source form
(for debugging or extending the library):

    - clone the
      Godafoss code repository http://www.github.com/wovo/godafoss-code
    - copy the godafoss directory to the root 
      of the target MicroPython device
      for instance using the file download funtion in Thonny

For working on the library a fast target with ample RAM is recommended.
My preferred target this is currently (2024) the Teensy 4.1
(a pity its MicroPython port doesn't have the nexopixel driver built in).



Use
---

Once installed, Godafoss can be used by importing it.
For the blinky below,
replace 42 with the number of the gpio pin that connects to
the LED on your target (5 for a...)::

    import godafoss as gf
    gf.blink( 42 )

Abstract data types
-------------------

The library uses abstractions for things like colors,
relative amounts, temperatures and coordinates.
These immutable abstract data classes are
:class:`~godafoss.color`,
:class:`~godafoss.fraction`,
:class:`~godafoss.temperature`,
:class:`~godafoss.xy`, and
:class:`~godafoss.xyz`.
When appropriate, objects of these classes support arithmetic operations
like addition, subtraction, multiplication and division.

Pins
---------

The library uses four types of pins: input, output, input_output,
and open collector.
An input pin has only a read() method, and output pin only a write() method.
An input_output pin and an open_collector pin have
both read() and write() methods.
An input_output pin also has methods to set the direction
to input or output.

+-------------------------------+----------+----------+-------------------------+
| class                         | read()   | write()  | direction_set_input()   |
|                               |          |          | direction_set_output()  |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_in`     |    x     |          |                         |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_out`    |          |    x     |                         |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_in_out` |    x     |    x     |     x                   |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_oc`     |    x     |    x     |                         |
+-------------------------------+----------+----------+-------------------------+

For an input_output pin, the appropriate direction_set method must be
called before a read() or write() method is called.
For an open_collector pin a low (zero, False) value written to the pin
is dominant, so a read() is meaningfull only after a high value (1, True) has
been written to the pin.

The preferred way to create a pin is to use one of the functions
:func:`~godafoss.make_pin_in()`,
:func:`~godafoss.make_pin_out()`,
:func:`~godafoss.make_pin_in_out()` or
:func:`~godafoss.make_pin_oc()`.
These functions return a pin object of the requested type.
These functions accept a board pin number or string, a pin object, or None.

When called with a hardware pin number or string,
the function returns a pin object that uses that hardware pin.
When called with a pin object, the function tries to create the requested
pin object from its argument.
When called with None, a dummy object of the appropriate type is returned.

Ports
----------

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
--------

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
--------

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
--------


image tool
font tool

Resource use
------------

On most MicroPython targets, RAM is a scarce.
To make the most of the available RAM the library uses on-demand loading:
most things within the library, and most attributes of its classes,
are loaded only when used.
This saves overall RAM, but at the cost of some overhead in loading time
and RAM for administration of the things thate are actually loaded .

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
-------

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

Code & other conventions
------------------------

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
---------------
"""
