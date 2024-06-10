# ===========================================================================
#
# file     : canvas__transformed.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================


import godafoss as gf

# ===========================================================================

class canvas__transformed( gf.canvas ):
    """
    helper class that is a transformed version of the canvas
    """

    def __init__( self, subject, size, transform_location ):
        self._subject = subject
        self._transform_location = transform_location
        gf.canvas.__init__(
            self,
            size = size,
            is_color = subject.is_color,
            background = subject._background
        )

    def write_pixel(
        self,
        location: gf.xy,
        ink: [ bool, None ] = True
    ) -> None:
        p = self._transform_location( location )
        if self._subject.within( p ):
            self._subject.write_pixel( p, ink )

    # =======================================================================

    def flush(
        self,
        forced: bool = False
    ) -> None:
        self._subject.flush( forced )

    # =======================================================================

    def clear( self, ink: bool = False ) -> None:
        self._subject.clear( ink )

    # =======================================================================

# ===========================================================================
