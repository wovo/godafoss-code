# ===========================================================================
#
# file     : rp2040.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

"""
rp2040
======

<picture>
Raspberry Pico: the first PCB module with an rp2040
wiki https://en.wikipedia.org/wiki/RP2040

+-------------------------------+-----------------------------------+
| CPU                           | 2 x Cortex-M0+                    |
+-------------------------------+-----------------------------------+
| Clock frequency`              | 133 MHz                           |
+-------------------------------+-----------------------------------+
| RAM`                          | 264 Kb                            |
+-------------------------------+-----------------------------------+
| FLASH`                        | external                          |
+-------------------------------+-----------------------------------+
| WiFi                          | no (external on Pico W)           |
+-------------------------------+-----------------------------------+
| USB                           | 1.1 host & device, DFU            |
+-------------------------------+-----------------------------------+
| MicroPython 1.22.2 free RAM`  | 227 Kb                            |
|                               | (185 Kb on Pico W)                |
+-------------------------------+-----------------------------------+
| MicroPython 1.22.2 free FLASH | depends on external flash chip    |
|                               | (1.4 Mb on Pico,                  |
|                               | 840 Kb on Pico W)                 |
+-------------------------------+-----------------------------------+

The rp2040 is the first and so far only micro-controller produced by
the Raspberry foundation. 
The chip has no on-chip flash memory:
it is used with an external serial flash chip.

The rp2040 supports Device Firmware Update over USB: powering the
chip with a certain pin pulled low puts has the
chip present itself as a mass storage device, 
to which a firmware file can simply be copied using the explorer.
Thonny uses this to provide an option to directly load a
micro-python image from the web to a connected rp2040 chip.

The rp2040 has, beside a normal set of hardware peripherals,
8 PIO state machines, which are very primitive but suprisingly
useable co-processors. These can be used to implement various
traditional (SPI, I2C) less traditional (one-wire, neopixel,
LCD) hardware peripherals. The library implements a few:
xxxx

The rp2040 is available as various PCB modules. 
The Raspberry Pico W adds WiFi, which is supported by
its specific micro-python version.
"""

