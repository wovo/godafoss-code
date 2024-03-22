# ===========================================================================
#
# file     : lib.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the code
#
# This file is part of the Godafoss perhiperal interface library.
#
# This script creates the combined tempdir/godafoss/__init__.py file
# by copying the directly-included submodules inline,
# imitting the godafoss includes.
#
# The indirectly-included submodules are copied to tempdir/godafoss.
#
# All files in tempdir/godafoss are cross-compiled to .mpy
# files in lib/godafoss. 
#
# ===========================================================================

import os, glob, sys, shutil, mpy_cross

def find_source_files( path ):
    results = []
    for entry in os.listdir( path ):
    
        if entry.endswith( ".py" ):
    
            destination = entry.replace( ".py", ".mpy" )
            
            # skip files that support running native (on the PC)
            if entry.find( "native" ) > -1:
                continue    
            
            # ignore the .py version of the __init__    
            if entry == "__init__.py":
                continue    
             
            # replace the __init__ with this __init_mpy, 
            # and put it one directory higher
            if entry == "__init__mpy.py":
                destination = "../__init__.mpy"

            results.append( [ path, entry, destination ] )
            
        elif ( entry.find( "." ) < 0 ):
        
            # ignore the tests
            if entry == "tests":
                continue
                
            results += find_source_files( path + "/" + entry )
            
    return results 


# ===========================================================================

def make_lib( mem_log ):

    try:
        shutil.rmtree( "../godafoss/lib" )
    except:
        pass
        
    os.makedirs( "../godafoss/lib/godafoss/g", exist_ok = True )
    
    for path, file, destination in find_source_files( "godafoss" ):
    
        source = path + "/" + file
        destination = \
            "../godafoss/lib/godafoss/g/" + destination
        
        s = f"python -m mpy_cross -o {destination} {source}"
        print( s )
        os.system( s )             
                   
    
# ===========================================================================

def run( args ):     
    mem_log = False
    for a in args[ 1 : ]:
        if a.lower() == "mem":
            mem_log = True        
    make_lib( mem_log )        

        
# ===========================================================================

if __name__ == "__main__":
    run( sys.argv )

    
# ===========================================================================
  