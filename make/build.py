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
    where <target> is rp2040, esp8266, esp32, or esp32c3
    requires: docker
    
    This command builds a micro-python image from the most recent 
    micro-python source, with godafoss included as frozen code.
    Docker is used, so on windows it must be running.
    
    When 'shell' is specified a bash prompt is opened.
    This might be usefull for debugging.
    
    The result (the micro-python image) is copied to the images directory.
"""


# ===========================================================================

def system( s: str ):
    print( "system:", s )
    os.system( s )
    
    
# ===========================================================================

def copy_result( container, source, destination ):
    system( 
        ( r"docker cp %s:" % container )
        + ( r"/work/micropython/ports/%s " % source )
        + ( r"images/%s" % destination )
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

    for file in glob.glob( "godafoss/**", recursive = True ):
        if file.endswith( ".py" ):
            # print( "include", file )
            dest = r"%s/modules/%s" % ( tempdir, file ) 
            dest = r"%s/modules/godafoss/g/%s" \
                % ( tempdir, os.path.basename( file ) ) 
            if os.path.basename( file ) == "__init__.py":
                dest = dest.replace( r"/g/", "/" )
            os.makedirs( os.path.dirname( dest ), exist_ok = True )
            shutil.copyfile( file, dest )
        
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
    if target == "esp8266":
        copy_result( 
            container, 
            "esp8266/build-ESP8266_GENERIC/firmware.bin", 
            "esp8266.bin" 
        )
    if target == "esp32":
        copy_result( 
            container, 
            "esp32/build-ESP32_GENERIC/firmware.bin", 
            "esp32.bin" 
        )
    if target == "esp32c3":
        copy_result( 
            container, 
            "esp32/build-ESP32_GENERIC_C3/firmware.bin", 
            "esp32c3.bin" 
        )



# ===========================================================================

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print( manpage )
        
    else:    
        target = sys.argv[ 1 ]
        if not target in [ "rp2040", "esp8266", "esp32", "esp32c3" ]:
            print( "unknown target" )
            
        else:
            shell = ( len( sys.argv ) > 2 ) and ( sys.argv[ 2 ] == "shell" )
            build( target, shell )
    
# ===========================================================================

    
