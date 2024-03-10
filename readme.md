Godafoss

https://wovo.github.io/godafoss/

What it is

Godafoss is a toolkit library for MicroPython (an implementation of 
the Python programming language for running on micro-controllers)
that makes programming a micro-controller easier and more portable 
by providing a consistent OO interface, and bundling drivers for 
a number of common peripherals.

After all, there are probably some libraries around that try to do this,
so why not add a new one (xkcd)?

For an introduction to using a micro-controller Godafoss library, 
check the tutorial.

import godafoss
godafoss.onboard_led.demo()

Features

- OO datatypes for color, fraction, xy, xyz
- OO pins & ports, including remote pins
- (extended) screenbuffer-based lcd/oled drivers
- drivers for various peripherals, with simple (test) demo's
- drivers take objects, not pin numbers

GPIO pins

The set of built-in drivers varies between MicroPython builds for
different targets. The library provides drivers for:

- color
- fraction
- xy, xyz

- pin_in, pin_out, pin_in_out, pin_oc
- port_in, port_out, port_in_out, port_oc
- pin_adc, pin_dac

- screenbuffer

- ws2818b one-pin serial addressable RGB LEDs
- ws2801 two-pin serial addressable RGB LEDs 
- apa102
- mrfc522 RFID card reader
- sr04 ultrasonic distace sensor
- ss1306 OLED
- pcf8764(a) I2C I/O extender
- pcf8591 I2C ADC/DAC
- 74hc595 shift register
- matrix keypad
- hobby servo
- max7219 LED matrix
- pca9685 LED dimmer & servo driver
- GPS module (NMEA)
- ina219
- https://github.com/sipeed/MaixPy K210
- amg8831 IR camera
- ov7670 camera
- color sensor
- nrf24
- CD4099 addressable latch
- ad7705
- ads1115
- ads1232
- hx711
- mcp23017
- hd44780 
- ESP8266 AT command set interface

Why the weird names, formatting, conventions, ...

- The library conforms to PEP8, except when I disagree with it.
- My personal language-independent naming convention is snake_case, 
  so that is what I use.
- I use type hints, eve though MicroPython doesn't support it
  yet. I hope it will someday.
- I use microseconds for delays and time durations. 
  Nanoseconds are a bit fast for a Python interpreter, and floats add
  overhead on chips that don't have floating point hardware, so this
  seems the best choice. Please use _ as 1000's separator to make
  your literals more readable: a second is 1_000_000 microseconds.

License

Godafoss uses the MIT license so you can do with it what you want,
except changing the license of the library itself, 
or sueing me when it doesn't work as expected.
The MIT license is NOT tainting, so code that uses the
library is not affected.
The MIT license text is part of the library, 
so you your application automatically includes the text, 
satisfying the requirement to include the license text.

Links

XKCD
Python
MicroPython
Thonny
uPyCraft
Raspberry Pi Pico
MIT license

https://docs.micropython.org/en/latest/library/index.html
https://docs.micropython.org/en/latest/library/pyb.html#constants