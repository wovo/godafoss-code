# ===========================================================================
#
# file     : canvas__part.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class canvas__part( gf.canvas ):
    """
        part of the canvas

        This method returns a new canvas that is
        part of the original canvas, as specified by the
        start and size parameters.

        The clear() method of a canvas part can be significantly slower
        than the clear() of the original canvas, because it can't use
        the clear() of the driver (which often has a fast way to clear
        the whole canvas).
    """

    def __init__(
        self,
        subject: gf.canvas,
        start: gf.xy,
        size: gf.xy
    ):
        self._subject = subject
        self._start = start
        gf.canvas.__init__(
            self,
            size,
            subject.is_color,
            subject._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, None ] = True
    ) -> None:
        self._subject.write_pixel( self._start + location, ink )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================
    #
    # can't use the subject clear() method, because that
    # would clear all of the subject.
    #
    # =======================================================================

# ===========================================================================
