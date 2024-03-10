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
            results.append( [ path, entry ] )
        elif ( entry.find( "." ) < 0 ) \
            and ( entry != "tests" ):
            results += find_source_files( path + "/" + entry )
    return results 


# ===========================================================================

def make_lib( mem_log ):

    try:
        shutil.rmtree( "lib/godafoss" )
    except:
        pass
        
    for path, file in find_source_files( "godafoss" ):
    
        source = path + "/" + file
        destination = "lib/" + path + "/" + file.replace( ".py", ".mpy" )
        os.makedirs( "lib/" + path, exist_ok = True )
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
  