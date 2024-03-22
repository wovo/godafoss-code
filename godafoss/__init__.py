# ===========================================================================
#
# file     : __init__.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in this file
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

import os

try:
    # present in standard Python, but not in MicroPython
    running_micropython = False
    
    _separator = os.sep
    
    # Micropython built-in
    const = lambda x: x
    uint = None
    
except:
    # so this must be MicroPython
    running_micropython = True
    
    _separator = "/"
    
    import time
    initial_time = time.ticks_us()
    
    import gc
    gc.collect()
    initial_free = gc.mem_free()
    
    from micropython import const

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

show_loading = False

from godafoss.tools.always import *


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

def __getattr__( name ):

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

    if show_loading:
        print( f"load element {name}" )

    try:
        # when frozen all files are lumped together in the godafoss directory
        # so no path is needed
        exec( f"from godafoss.g.{name} import {name}" )
    
    except ImportError:
    
        try:
            # try to find the file in the godafoss tree
            found = _import_path( _path, name )
            
        except:
        
            # mimic the original error
            exec( f"from godafoss.g.{name} import {name}" )        

        if found is None:
            raise AttributeError( f"unknown class '{name}'" ) from None

        exec( f"from {found} import {name}" )
        
    _loaded_attributes[ name ] = f = eval( name )
    return f


# ===========================================================================
#
# Inherit this class to get autoloading of class attributes from
# <class_name>__<method_name>.<_suffix> files.
# The attribute must be a function or class named
# <class_name>__<method_name>.
# The loaded attribute is added to the class, so on subsequent use
# it will be used directly.
#
# ===========================================================================

class autoloading:

    def __init__(
        self,
        class_type: type
    ):
        self._class_type = class_type
        self._class_name = class_type.__name__

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
            print( f"from godafoss.g.{name} import {name}" )
            exec( f"from godafoss.g.{name} import {name}" )
            
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


# ===========================================================================
