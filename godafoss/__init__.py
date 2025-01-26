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
# This is the root file of the Godafoss library.
# To avoid the memory footprint required to (always) load all library parts,
# the __getattr__() function loads godafoss attributes on request,
# and classes that inherit autoloading will load methods on request.
#
# Dividing code over different files saves memory when not all files
# are loaded, but a loaded file adds an overhead of ~200 bytes.
# For comparison, a simple function like clamp takes ~70 bytes.
# For this reason number of small functions and classes are
# in this __init__.py file.
#
# To show the initially available ram in Thonny, put this line in a file
# an run it in a fresh interpreter
#     import gc; print( gc.mem_free() )
# Note: running it directly at the prompt gives a lower value.
#
# This file also contains a literal copy of the (MIT) license text,
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
Copyright 2024 Wouter van Ooijen (wouter@voti.nl)

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

import os
   

try:
    # present in standard Python, but not in MicroPython
    _separator = os.sep

    running_micropython = False

    # Micropython built-in
    const = lambda x: x
    uint = None

    import time
    initial_time = time.monotonic_ns() // 1000

except AttributeError:
    # so this must be MicroPython
    running_micropython = True

    _separator = "/"

    import time
    initial_time = time.ticks_us()

    import gc
    gc.collect()
    initial_free = gc.mem_free()

    from micropython import const



# ===========================================================================

try:
    # the root of the godafoss library is where this file is
    _path = __file__[  : __file__.rfind( _separator ) ]

    # the name of the library (should be 'godafoss',
    # but it might be installed under a different name)
    _library = _path[ _path.rfind( _separator ) + 1 : ]

    # used when looking for files. can be .py or .mpy
    # but the compiled version has the .my suffix ;)
    _suffix = __file__[ __file__.rfind( "." ) : ]

except:
    pass


# ===========================================================================

show_loading = False

# $$document( 0 )
from godafoss.basics import *
from godafoss.adts import *
from godafoss.interfaces import *
from godafoss.pins import *
from godafoss.gpio import *
from godafoss.ports import *
from godafoss.edge import *
#from godafoss.canvas import *
#from godafoss.shapes import *
#from godafoss.fonts import *
from godafoss.terminal import *

from godafoss.chips.lcds.hd44780 import *
#from godafoss.displays import *
#from godafoss.targets import *


#from godafoss.chips.gpio_expanders.pcf8574 import *


# $$document( 1 )

# ===========================================================================
#
# Look below <path> for the Python file <name> (without suffix).
# If found, return the Python import path for this file,
# else return None.
#
# ===========================================================================

def _import_path( path, name ):
    """
    Look below <path> for the Python file <name> (without suffix).
    If found, return the Python import path for this file,
    else return None.
    """

    # print( "find", path, name )

    for entry in os.listdir( path ):

        # look for a file with the same suffix as we have
        if entry == name + _suffix:
            # create the (relative) Python path from the
            # (absolute) file path + name
            return _library + "." \
                + path[ len( _path ) + 1 : ].replace( _separator, "." ) \
                + "." + entry.replace( _suffix, "" )

        # if the entry has no '.' in it,
        # assume it to be a (sub)directory that must be searched
        if entry.find( "." ) < 0:
            result = _import_path( path + _separator + entry, name )
            if result is not None:
                return result

    return None


# ===========================================================================
#
# The __getattr__ function is called when something inside godafoss
# is requested (like godafoss.something) which is not (yet) present.
# The function looks for a file within the godafoss library with the name
# equal to what was requested, and (attempts to) load the requested thing
# from that file and return it.
#
# Note: The code below works on both native Python and Micropython.
# On MicroPython, loading a module inside a function actually loads
# it into the surrounding module. This could be used to simplify the code
# somewhat, but that would loose the possibility to run on native Python.
#
# ===========================================================================

_loaded_attributes = {}

def _x_getattr__( name ):

    # =======================================================================
    #
    # already present? just return it
    #
    # =======================================================================

    try:
        return _loaded_attributes[ name ]
    except:
        pass

    # =======================================================================
    #
    # not present? try to load, save, and return it
    #
    # =======================================================================

    import gc; gc.collect()

    if True: # show_loading:
        print( f"load element {name}" )

    try:
        # when frozen all files are lumped together in the godafoss directory
        # so no path is needed
        exec( f"from godafoss.gf.{name} import {name}" )

    except ImportError:

        try:
            # try to find the file in the godafoss tree
            found = _import_path( _path, name )

        except:

            # mimic the original error
            exec( f"from godafoss.gf.{name} import {name}" )

        if found is None:
            raise AttributeError( f"unknown class '{name}'" ) from None

        exec( f"from {found} import {name}" )

    _loaded_attributes[ name ] = f = eval( name )
    return f


# ===========================================================================


