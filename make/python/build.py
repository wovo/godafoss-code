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

# a docker error should halt the process
# spiram now only for s3

import mpy_cross
import sys
import os
import glob
import shutil
from distutils.dir_util import copy_tree

sys.path.append( "." )
import godafoss


# ===========================================================================
#
# docker fragments
# 
# ===========================================================================

docker_common = """

# ===========================================================================
#
# common for all targets
#
# ===========================================================================

FROM ubuntu

RUN apt update
RUN apt install -y git wget make cmake build-essential ninja-build ccache 
RUN apt install -y flex bison gperf 
RUN apt install -y libffi-dev libssl-dev dfu-util libusb-1.0-0
RUN apt install -y python3 python3-pip python3-venv python-is-python3

WORKDIR /work
RUN git clone https://www.github.com/micropython/micropython

WORKDIR /work/micropython
RUN make -C mpy-cross

$$toolchain

# ===========================================================================
#
# build
#
# ===========================================================================

WORKDIR /work/micropython/shared/runtime
$$sedline

WORKDIR /work/micropython/ports/$$port
RUN cp /startup run
RUN echo "make submodules" >> run
RUN bash ./run

WORKDIR /work/micropython/ports/$$port/modules
COPY modules .

WORKDIR /work/micropython/ports/$$port
RUN cp /startup run
RUN echo "make board=$$board" >> run
RUN bash ./run


# ===========================================================================
#
# to inspect the result
#
# ===========================================================================

CMD [ "bash" ]  

"""

# ===========================================================================

docker_arm = """

# ===========================================================================
#
# ARM toolchain
#
# ===========================================================================

RUN apt install -y gcc-arm-none-eabi libnewlib-arm-none-eabi 
RUN echo " " > /startup

""" 

# ===========================================================================

docker_esp8266 = """

# ===========================================================================
#
# ESP8266 toolchain
#
# ===========================================================================

WORKDIR /esp
RUN wget https://github.com/jepler/esp-open-sdk/releases/download/2018-06-10/xtensa-lx106-elf-standalone.tar.gz
RUN tar zxvf xtensa-lx106-elf-standalone.tar.gz
RUN rm xtensa-lx106-elf/bin/esptool.py  # Use system version of esptool.py instead.
RUN pip install --break-system-packages esptool
RUN echo "export PATH=/esp/xtensa-lx106-elf/bin/:$PATH" > /startup

""" 

# ===========================================================================

docker_esp32 = """

# ===========================================================================
#
# ESP32 Xtensa toolchain
#
# ===========================================================================

WORKDIR /esp
RUN git clone -b v5.0.4 --recursive https://github.com/espressif/esp-idf.git
WORKDIR /esp/esp-idf
RUN ./install.sh all
RUN echo "source /esp/esp-idf/export.sh" > /startup
""" 


# ===========================================================================
#
# target descriptions
#
# ===========================================================================

targets = {}

class target:
    def __init__( 
        self,
        name,
        port,
        board,
        toolchain,
        result,
        image
    ):
        self.name = name
        self.port = port
        self.toolchain = toolchain
        self.board = board
        self.result = result        
        self.image = image
        
        self.dockerscript = docker_common\
            .replace( "$$toolchain", self.toolchain ) \
            .replace( "$$port", self.port ) \
            .replace( "$$board", self.board ) \
            
        targets[ self.name ] = self    
    
    
# ===========================================================================

# PI pico and relatives
target(     
    name = "rp2040",
    port = "rp2",
    board = "RPI_PICO",
    toolchain = docker_arm,
    result = "rp2/build-RPI_PICO/firmware.uf2", 
    image = "rp2040$$suffix.uf2" 
)
target(     
    name = "rp2040w",
    port = "rp2",
    board = "RPI_PICO_W",
    toolchain = docker_arm,
    result = "rp2/build-RPI_PICO/firmware.uf2", 
    image = "rp2040$$suffix.uf2" 
)

# teensies
target(
    name = "teensy40",
    port = "mimxrt",
    board = "TEENSY40",
    toolchain = docker_arm,
    result = "mimxrt/build-TEENSY40/firmware.hex", 
    image = "teensy40$$suffix.hex" 
)
target(
    name = "teensy41",
    port = "mimxrt",
    board = "TEENSY41",
    toolchain = docker_arm,
    result = "mimxrt/build-TEENSY40/firmware.hex", # weird
    image = "teensy41$$suffix.hex" 
)

# esp8266 L106, requires some hacks
target(
    name = "esp8266",
    port = "esp8266",
    board = "ESP8266_GENERIC",
    toolchain = docker_esp8266, 
    result = "esp8266/build-ESP8266_GENERIC/firmware.bin", 
    image = "esp8266$$suffix.bin" 
)

# esp32 Xtensa
target(
    name = "esp32",
    port = "esp32",
    board = "ESP32_GENERIC",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32$$suffix.bin" 
)
target(
    name = "esp32s2",
    port = "esp32",
    board = "ESP32_GENERIC_S2",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32s2$$suffix.bin" 
)
target(
    name = "esp32s3",
    port = "esp32",
    board = "ESP32_GENERIC_S3",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32s3$$suffix.bin" 
)
target(
    name = "esp32s3-spiram",
    port = "esp32",
    board = "ESP32_GENERIC_S3-SPIRAM_OCT",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32s3-spiram$$suffix.bin" 
)

# esp32 RISC V
target(
    name = "esp32c2",
    port = "esp32",
    board = "ESP32_GENERIC_C2",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32c2$$suffix.bin" 
)
target(
    name = "esp32c3",
    port = "esp32",
    board = "ESP32_GENERIC_C3",
    toolchain = docker_esp32, 
    result = "esp32/build-ESP32_GENERIC/firmware.bin", 
    image = "esp32c3$$suffix.bin" 
)

"""
    target(
        "esp32s3-spiram",
        docker_esp32, 
        "",
        "esp32/build-ESP32_GENERIC_S3-SPIRAM_OCT/firmware.bin", 
        "esp32s3$$suffix.bin" 
    )
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
        
            # skip documentation files
            if entry == "docs":
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
    t: target,
    gf: bool = True,
    shell: bool = False,
):

    print( f"build {t.name}" )

    # create fresh work directory
    workdir = r"temp/build"
    try:
        shutil.rmtree( workdir )
    except:
        pass     
        
    # get godafoss library files if gf == True
    # but always create the directory
    for path, file, destination in find_source_files( "godafoss" ):
    
        source = path + "/" + file
        destination = \
            workdir + "/modules/godafoss/gf/" + destination
        destination = destination.replace( ".mpy", ".py" )
        
        os.makedirs( os.path.dirname( destination ), exist_ok = True )
        if gf:    
            shutil.copyfile( source, destination )
            
    dockerscript = t.dockerscript   
    
    # shared\runtime\pyexec.c
    # before #if MICROPY_PY_BUILTINS_HELP
    # insert mp_hal_stdout_tx_str("with godafoss\r\n");    
    
    target = "/#if MICROPY_PY_BUILTINS_HELP/amp_hal_stdout_tx_str("
    notice = f"with godafoss {godafoss.version}"
    sedline = f"RUN sed -i '{target}\"{notice}\\\\r\\\\n\");' pyexec.c" 
    if not gf:
        sedline = ""
    dockerscript = dockerscript.replace( 
       "$$sedline",  
       sedline
    )   
    
    with open( f"{workdir}/dockerfile", "w" ) as f:
        f.write( dockerscript )
    
    image = f"godafoss_{t.name}_image"
    system( f"docker build -t {image} {workdir}" )
    
    container = f"godafoss_{t.name}_container"
    system( f"docker rm {container}" ) 
    
    flags = "-it" if shell else ""
    system( r"docker run --name %s %s %s" % ( container, flags, image ) ) 
    
    suffix = "-gf" if gf else "-nogf"
        
    copy_result( 
        container, 
        t.result, 
        t.image.replace( "$$suffix", suffix )
    )


# ===========================================================================

manpage = """
usage: make/build { <target> | all | nogf | gf [ shell }
    where <target> is one of
$$targets 
    requires: docker
    
    This command builds a micro-python image for the specified target
    (or for all targets) from the most recent micro-python source, 
    with godafoss included as frozen code (gf) or not (nogf).
    Docker is used, so on windows it must be running.
    
    When 'shell' is specified a bash prompt is opened.
    This might be usefull for debugging.
    
    The result (the micro-python image) is copied to the images directory
    of the godafoss website, which is assumed to be at ../godafoss/images
"""

# ===========================================================================

def main():

    print( "start" )

    if len( sys.argv ) < 2:
        prefix = 8 * " "
        s = ""
        line = prefix
        for t in sorted( list( targets ) ) + [ "all" ]:
            if len( line + t ) > 78:
                s = line + "\n"
                line = prefix
            line = line + t + " "
        s = s + line
        print( manpage.replace( "$$targets", s ) )
        return
        
    gf = {}
    shell = False
    target = []
    for arg in sys.argv[ 1 : ]:
        if arg == "all":
            target = targets.keys()
            
        elif arg in targets.keys():
            if not arg in target:
                target.append( arg )
                
        elif arg == "gf":
            gf[ True ] = None
            
        elif arg == "nogf":
            gf[ False ] = None
            
        elif arg == "both":
            gf[ True ] = None
            gf[ False ] = None
            
        elif arg == "shell":    
            shell = True
            
        elif arg == "noshell":
            shell == False
            
        else:
            print( f"unknown argument {arg}" )
            return
            
    if gf == {}:
        print( "specify gf, nogf or both" )
        return
        
    print( "5", target, gf )    
        
    for t in sorted( list( target ) ):
        print( "6", t, gf.keys() )
        for g in gf.keys():
            print( "gona build", g )
            build( targets[ t ], g, shell )
    
    
# ===========================================================================

print( "1" )
if __name__ == '__main__':
    print( "2" )
    main()


# ===========================================================================
