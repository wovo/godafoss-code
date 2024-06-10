# ===========================================================================
#
# file     : targets.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

targets = None

#$$document( 0 )

"""

The library can be used on all MicroPython ports.
The table below shows the target chips and boards
on which I tested the library, and their key features.
Most targets have a dedicated description.

import gc; gc.collect(); gc.mem_free()

CPU
Clock
RAM
FLASH
MicroPython free RAM
MicroPython free FLASH
Notes


+-------------------------------+----------+----------+-------------------------+
| Microcontroller                         | read()   | write()  | direction_set_input()   |
|                               |          |          | direction_set_output()  |
+-------------------------------+----------+----------+-------------------------+
| :class:`~`     |    x     |          |                         |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_out`    |          |    x     |                         |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_in_out` |    x     |    x     |     x                   |
+-------------------------------+----------+----------+-------------------------+
| :class:`~godafoss.pin_oc`     |    x     |    x     |                         |
+-------------------------------+----------+----------+-------------------------+


"""

