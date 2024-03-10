# ===========================================================================
#
# file     : canvas__inverted.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

# ===========================================================================

def _invert_ink( ink: [ bool, gf.color ] ):
    return not ink if isinstance( ink, bool ) else - ink

# ===========================================================================

class canvas__inverted( gf.canvas ):
    """
    inverse of the display

    This method returns a display that inverts the effect
    of write_pixel() calls.
    """

    def __init__(
        self,
        subject: gf.canvas
    ):
        self._subject = subject
        gf.canvas.__init__(
            self,
            subject.size,
            subject.is_color,
            subject._background
        )

    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
        ink: [ bool, gf.color ]
    ) -> None:
        self._subject.write_pixel(
            location,
            _invert_ink( ink )
        )

    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================


# ===========================================================================
