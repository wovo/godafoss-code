# ===========================================================================
#
# file     : __init__.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (godafoss.license)
#
# ===========================================================================
#
# This file contains a literal copy of the (MIT) license text,
# which fulfills the requirement of this license that a copy
# of its text is included in all software it applies to.
#
# ===========================================================================

__version__ = "1.0"
__author__ = "wouter van Ooijen (wouter@voti.nl)"

version = __version__


# ===========================================================================
#
# MIT license text
#
# ===========================================================================

license = """
Copyright 2024, 2025 Wouter van Ooijen (wouter@voti.nl)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


# ===========================================================================

# $$document( 0 )

from godafoss.gf_basics import *
from godafoss.gf_adts import *
from godafoss.gf_interfaces import *
from godafoss.gf_gpio import *
from godafoss.gf_pins import *
from godafoss.gf_ports import *
from godafoss.gf_edge import *
from godafoss.gf_canvas import *
from godafoss.gf_shapes import *
from godafoss.gf_fonts import *
from godafoss.gf_terminal import *
from godafoss.gf_lcds import *
from godafoss.gf_chips_ssd import *
from godafoss.gf_chips_touch import *
from godafoss.gf_chips_uc8151 import *
from godafoss.gf_chips_misc import *
from godafoss.gf_displays import *
from godafoss.gf_boards import *

# $$document( 1 )


# ===========================================================================


