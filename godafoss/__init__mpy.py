# ===========================================================================
#
# file     : __init__mpy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in this file
#
# ===========================================================================
#
# This is the root file of the Godafoss library when running as .mpy
# (as installed library, or as frozen code in the micropython image.
#
# For the explanation behing this file, check the comment in __init__.py.
# This version is simpler, because it relies on all files being in
# the godafoss/g sub directory.
#
# ===========================================================================

running_micropython = True
    
import time
initial_time = time.ticks_us()

import gc
gc.collect()
initial_free = gc.mem_free()

from micropython import const

show_loading = False

from godafoss.g.always import *

# ===========================================================================

_loaded_attributes = {}

def __getattr__( name ):

    try:
        return _loaded_attributes[ name ]
    except:
        pass

    import gc; gc.collect()

    if show_loading:
        print( f"load element {name}" )

    exec( f"from godafoss.g.{name} import {name}" )
    
    _loaded_attributes[ name ] = f = eval( name )
      
    return f


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
            
        exec( f"from godafoss.g.{name} import {name}" )
                   
        func = constructor = eval( f"{name}" )

        if isinstance( func, type ):
            func = lambda *args, **kwargs: constructor( *args, **kwargs )

        setattr( self._class_type, obj, func )

        return lambda *args, **kwargs: func( self, *args, **kwargs )


# ===========================================================================
