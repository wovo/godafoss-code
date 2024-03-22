# ===========================================================================
#
# file     : build.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the giodafioss __init__.py
#
# ===========================================================================
#
# Build a micro-python image that includes godafoss.
#
# ===========================================================================

import mpy_cross
import sys
import os
import glob
import shutil
from distutils.dir_util import copy_tree


# ===========================================================================

manpage = """
usage: make/build <target> [shell]
    where <target> is 
        rp2040, teensy41, esp8266, esp32, esp32s3, esp32c3, 
        or all
    requires: docker
    
    This command builds a micro-python image for the specified target
    (or for all targets) from the most recent micro-python source, 
    with godafoss included as frozen code.
    Docker is used, so on windows it must be running.
    
    When 'shell' is specified a bash prompt is opened.
    This might be usefull for debugging.
    
    The result (the micro-python image) is copied to the images directory.
"""


# ===========================================================================

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

def system( s: str ):
    print( "system:", s )
    os.system( s )
    
    
# ===========================================================================

def copy_result( container, source, destination ):
    os.makedirs( "../godafoss/images", exist_ok = True )
    system( 
        ( r"docker cp %s:" % container )
        + ( r"/work/micropython/ports/%s " % source )
        + ( r"../godafoss/images/%s" % destination )
    )    

    
# ===========================================================================

def build( 
    target: str,
    shell: bool = False
):

    # shell = True

    tempdir = r"temp/build/%s" % target

    try:
        shutil.rmtree( tempdir )
    except:
        pass
    #copy_tree( 
    #    r"make/docker/build_%s" % target, 
    #    r"tempdir\build\build_%s" % target 
    #)
    #os.makedirs( r"%s/modules/godafoss" % tempdir )

    for path, file, destination in find_source_files( "godafoss" ):
    
        source = path + "/" + file
        destination = \
            tempdir + "/modules/godafoss/g/" + destination
        destination = destination.replace( ".mpy", ".py" )
        
        os.makedirs( os.path.dirname( destination ), exist_ok = True )
        shutil.copyfile( source, destination )
        
    shutil.copyfile( 
        "make/dockers/%s/dockerfile" % target, 
        "%s/dockerfile" % tempdir 
    )
    
    image = r"godafoss_%s_image" % target
    system( r"docker build -t %s %s" % ( image, tempdir ) )
    
    container = r"godafoss_%s_container" % target
    system( r"docker rm %s" % container ) 
    
    flags = "-it" if shell else ""
    system( r"docker run --name %s %s %s" % ( container, flags, image ) ) 
        
    if target == "rp2040":
        copy_result( 
            container, 
            "rp2/build-RPI_PICO/firmware.uf2", 
            "rp2040.uf2" 
        )
    elif target == "teensy41":
        copy_result( 
            container, 
            "mimxrt/build-TEENSY40/firmware.hex", 
            "teensy41.hex" 
        )
    elif target == "esp8266":
        copy_result( 
            container, 
            "esp8266/build-ESP8266_GENERIC/firmware.bin", 
            "esp8266.bin" 
        )
    elif target == "esp32":
        copy_result( 
            container, 
            "esp32/build-ESP32_GENERIC/firmware.bin", 
            "esp32.bin" 
        )
    elif target == "esp32c3":
        copy_result( 
            container, 
            "esp32/build-ESP32_GENERIC_C3/firmware.bin", 
            "esp32c3.bin" 
        )
    elif target == "esp32s3":
        copy_result( 
            container, 
            "esp32/build-ESP32_GENERIC_S3/firmware.bin", 
            "esp32s3.bin" 
        )
    else:
        print( "unknown target {target}"     )


# ===========================================================================

targets = [ 
    "rp2040", 
    "teensy41", 
    "esp8266", 
    "esp32", 
    "esp32c3",
    "esp32s3",
]

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print( manpage )
        
    else:    
        target = sys.argv[ 1 ]
        if not target in targets + [ "all" ]:
            print( "unknown target" )
            
        else:
            shell = ( len( sys.argv ) > 2 ) and ( sys.argv[ 2 ] == "shell" )
            if target == "all":
                for target in targets:
                    build( target, shell )
            else:
                build( target, shell )
    
# ===========================================================================

    
