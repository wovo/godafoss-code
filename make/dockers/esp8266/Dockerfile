# ===========================================================================
#
# file     : make/docker/esp8266/Dockerfile
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the giodafioss __init__.py
#
# ===========================================================================
#
# This docker builds the MicroPython + godafoss image for the esp8266.
#
# ===========================================================================


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
RUN apt install -y python3 python3-pip python3-venv

WORKDIR /work
RUN git clone https://www.github.com/micropython/micropython

WORKDIR /work/micropython
RUN make -C mpy-cross


# ===========================================================================
#
# ESP toolchain
#
# ===========================================================================

WORKDIR /esp
RUN wget https://github.com/jepler/esp-open-sdk/releases/download/2018-06-10/xtensa-lx106-elf-standalone.tar.gz
RUN tar zxvf xtensa-lx106-elf-standalone.tar.gz
RUN rm xtensa-lx106-elf/bin/esptool.py  # Use system version of esptool.py instead.
RUN pip install esptool


# ===========================================================================
#
# build
#
# ===========================================================================

WORKDIR /work/micropython/ports/esp8266/modules
COPY modules .
RUN rm godafoss/g/board*
RUN rm godafoss/g/unit_test*
RUN rm godafoss/g/rp2040*
RUN rm godafoss/g/esp32*


WORKDIR /work/micropython/ports/esp8266
RUN echo "export PATH=/esp/xtensa-lx106-elf/bin/:$PATH" > run
RUN echo "make submodules" >> run
RUN echo "make -j BOARD=ESP8266_GENERIC" >> run
RUN bash ./run


# ===========================================================================
#
# to inspect the result
#
# ===========================================================================

CMD [ "bash" ]  

# ===========================================================================
