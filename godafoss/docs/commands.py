# ===========================================================================
#
# file     : commands.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

commands = None

#$$document( 0 )

"""
development commands
--------------------

The commands described below support godafoss development work.
The commands assume you cloned the godafosss repository,
and are in a command window (windows powershell or linux bash)
at the root of the repository.

make/build
    usage: make/build <target>
    Build a micro-python image with godafoss for <target>
    in the images directory.
    Requires: mpy

make/clean
    usage: make/clean
    Removes __pycache__ files from the godafoss sources.
    Do this to save time when loading the sources to a target.

make/gff
make/glyph

make/html
    usage: make/html
    Build the html documentation in the docs directory.
    Requires: sphynx

make/json

make/lib
    usage: make/lib
    Build the precompiled (.mpy) version of the library in lib/godafoss.

make/load
    usage: make/load <target>
    Load the image from images directory into the target chip.
    Requires: mpy-load (esp32)

make/pdf:
    under construction

make/pull
    usage: make/pull

make/push
    uage: make/push
    Push to git (message: "update")

make/release
    usage: make/release
    Prepare a release push: make/clean, make/html, make/lib, make/build
    for the supported targets.

make/test
    usage: make test
    Run the (hosted) tests, test coberage, and style checks.
"""
