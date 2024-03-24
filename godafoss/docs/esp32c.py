# ===========================================================================
#
# file     : esp32c.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

esp32c = None

"""

+------------------------+------------------+
| CPU                    | 2 x Cortex-M0    |
+------------------------+------------------+
| Clock frequency`       | 166 MHz          |
+------------------------+------------------+
| RAM`                   | 254 Kb           |
+------------------------+------------------+
| FLASH`                 | external         |
+------------------------+------------------+
| MicroPython free RAM`  | 166 Kb           |
+------------------------+------------------+
| MicroPython free FLASH | 120 Kb           |
+------------------------+------------------+

The rp2040 is the first and so far only micro-controller produced by


"""

