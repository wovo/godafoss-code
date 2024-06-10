# ===========================================================================
#
# file     : lib.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the code
#
# All files are cross-compiled to .mpy
# files in ../godafoss/godafoss
# and the ../godafoss/package.json is created.
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

json_template = """{
    "homepage": "https://github.com/wovo/godafoss",
    "license": "MIT-0",
    "description": "A MicroPython library",
    "repository": {
        "type": "git",
        "url": "https://github.com/wovo/godafoss-code"
    },
    "version": "0.1",
    "urls": [
        %files%
    ]
}
"""

def make_lib( mem_log ):

    try:
        shutil.rmtree( "../godafoss/godafoss" )
    except:
        pass
        
    os.makedirs( "../godafoss/godafoss/gf", exist_ok = True )
    
    files = ""
    separator = ""
    for path, file, destination in find_source_files( "godafoss" ):
    
        files += f"""{separator}
        [ 
            "godafoss/gf/{destination}", 
            "github:wovo/godafoss/godafoss/gf/{destination}" 
        ]"""
        separator = ","
        
        source = path + "/" + file
        destination = \
            "../godafoss/godafoss/gf/" + destination
        
        s = f"python -m mpy_cross -o {destination} {source}"
        print( s )
        os.system( s )    

    with open( "../godafoss/package.json", "w" ) as f:
        f.write( json_template.replace( "%files%", files ) )
                   
    
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
  