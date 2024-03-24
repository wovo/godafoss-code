# ===========================================================================
#
# file     : esp8266.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

esp8266 = None

"""
esp8266
=======

<image>
Wemos D1 esp8266 module with serial interface
wiki https://en.wikipedia.org/wiki/ESP8266

+------------------------+---------------------------------+
| CPU                    | Tenscilica L 106                |
+------------------------+---------------------------------+
| Clock frequency`       | 60 or 180 MHz                   |
+------------------------+---------------------------------+
| RAM`                   | 160 Kb                          |
+------------------------+---------------------------------+
| FLASH`                 | external                        |
+------------------------+---------------------------------+
| WiFi                   | yes                             |
+------------------------+---------------------------------+
| USB                    | none                            |
+------------------------+---------------------------------+
| MicroPython free RAM`  | xxx Kb                          |
+------------------------+---------------------------------+
| MicroPython free FLASH | depends on external flash chip  |
+------------------------+---------------------------------+

The esp8266 was the first micro-controller with builkt-in WiFi that
was both cheap and easily available.
It can be found in a wide variety of modules and PCBs, and in low-cost
WiFi connected consumer products like intelligent light bulbs.

The chip has no on-chip flash memory:
it is used with an external serial flash chip.
The esp8285 is a close equivalent with 1 MB flash memory on the chip.

For new projects, the esp32 should ve preferred.

The esp8266 can be used with the library, but it is slow.
The amount if RAM is far too low to use the library in source form.
With the library included in the image, simple applications
can be run, but the start-up time can be 10s of seconds.
"""

