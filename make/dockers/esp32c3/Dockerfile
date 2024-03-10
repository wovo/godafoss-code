# ===========================================================================
#
# file     : make/docker/esp32c3/Dockerfile
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the giodafioss __init__.py
#
# ===========================================================================
#
# This docker builds the MicroPython + godafoss image for the esp32c3.
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
RUN git clone -b v5.0.4 --recursive https://github.com/espressif/esp-idf.git
WORKDIR /esp/esp-idf
RUN ./install.sh all
# source /esp/esp-idf/export.sh


# ===========================================================================
#
# build
#
# ===========================================================================

WORKDIR /work/micropython/ports/esp32
RUN echo "source /esp/esp-idf/export.sh" > run
RUN echo "make submodules" >> run
RUN bash ./run

WORKDIR /work/micropython/ports/esp32/modules
COPY modules .
RUN rm godafoss/g/*rp2040*

WORKDIR /work/micropython/ports/esp32
RUN echo "source /esp/esp-idf/export.sh" > run
RUN echo "make BOARD=ESP32_GENERIC_C3" >> run
RUN bash ./run


# ===========================================================================
#
# to inspect the result
#
# ===========================================================================

CMD [ "bash" ]  

# ===========================================================================
