# ===========================================================================
#
# file     : make/docker/rp2040/Dockerfile
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the giodafioss __init__.py
#
# ===========================================================================
#
# This docker builds the MicroPython + godafoss image for the rp2040.
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
# ARM toolchain
#
# ===========================================================================

RUN apt install -y gcc-arm-none-eabi libnewlib-arm-none-eabi 


# ===========================================================================
#
# build
#
# ===========================================================================

WORKDIR /work/micropython
RUN git submodule update --init -- lib/pico-sdk
RUN git submodule update --init -- lib/tinyusb

WORKDIR /work/micropython/lib/pico-sdk
RUN git submodule update --init

WORKDIR /work/micropython/ports/rp2
RUN make board=PICO submodules

WORKDIR /work/micropython/ports/rp2/modules
COPY modules .

WORKDIR /work/micropython/ports/rp2
RUN make board=PICO


# ===========================================================================
#
# to inspect the result
#
# ===========================================================================

CMD [ "bash" ]

# ===========================================================================
