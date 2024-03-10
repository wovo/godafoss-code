# ===========================================================================
#
# file     : ggf.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class ggf( gf.shape ):
    """
    read a shape from a ggf file

    :param: file_name: str
        file that contains the image data in ggf format

    :param: cached: bool
        whether the file content is read into RAM at construction
        (default: False)

    This is a shape object that is read from a ggf format file stored
    on the target.
    By default, the file content is read into RAM when the ggf object is
    constructed.
    When cached is False, the file data is read (but not permanently stored)
    when the ggf object is written to a canvas. This is slower, but
    saves RAM.

    The Godafoss Graphic Format (ggf) is a very simple uncompressed
    graphic file format.
    The ggf.py script (in the make directory of the godafoss github)
    can be used to create ggf files from any graphic format readable
    by PIL.

    +----------------------------------------------------------------+
    | ggf format                                                     |
    +-----------+----------------+-----------------------------------+
    | byte 0    | identification | 0xA6                              |
    +-----------+----------------+-----------------------------------+
    | byte 1    | pixel format:  | 0: 1 bit/pixel MSB first          |
    |           |                +-----------------------------------+
    |           |                | 1: 1-byte RGB 3,3,2 R first       |
    |           |                +-----------------------------------+
    |           |                | 2: 3-byte RGB R first             |
    +-----------+----------------+-----------------------------------+
    | bytes 2-3 | x pixels size  | high byte first                   |
    +-----------+----------------+-----------------------------------+
    | bytes 4-5 | y pixels size  | high byte first                   |
    +-----------+----------------+-----------------------------------+
    | bytes 6.. | pixel data     | by row; for B/W the last byte of  |
    |           |                | each row is padded to a full byte |
    +-----------+----------------+-----------------------------------+
    """

    # =======================================================================

    def __init__(
        self,
        file_name: str,
        cached: bool = True
    ) -> None:

        gf.shape.__init__( self )

        if not file_name.endswith( ".ggf" ):
            file_name += ".ggf"
        f = open( file_name, "rb" )

        x = f.read( 1 )[ 0 ]
        if x != 0xA6:
            raise valueError(
                "file %s first byte %02X, should be 0xA6"
                % ( file_name, x ) )

        self.depth = f.read( 1 )[ 0 ]
        if not self.depth in [ 0, 1, 2 ]:
            raise ValueError(
                "file %s depth byte %d, should be 0,1,2"
                % ( file_name, depth ) )

        s = f.read( 2 )
        x = s[ 0 ] * 256 + s[ 1 ]
        s = f.read( 2 )
        y = s[ 0 ] * 256 + s[ 1 ]
        self.size = xy( x, y )

        if cached:
            self.data = f.read( x * y * 3 )
            self.write = self._write_cached
        else:
            self.file_name = file_name
            self.write = self._write_from_file

        f.close()

    # =======================================================================

    def _write_cached(
        self,
        c: gf.canvas,
        offset: gf.xy = gf.xy( 0, 0 )
    ):
        i = 0
        for y in range( self.size.y ):
            for x in range( self.size.x ):

                if self.depth == 0:
                    if ( x % 8 ) == 0:
                        v = self.data[ i ]
                        i += 1
                    c.write_pixel( offset + gf.xy( x, y ), v & 0x01 != 0x00 )
                    v = v >> 1

                elif self.depth == 1:
                    d = f.read( 1 )[ 0 ]
                    r = (( d >> 5 ) & 0x07 ) << 5
                    g = (( d >> 2 ) & 0x07 ) << 5
                    b = (( d >> 0 ) & 0x03 ) << 6
                    c.write_pixel( offset + gf.xy( x, y ), color( r, g, b ) )

                else:
                    p = color(
                        self.data[ i ],
                        self.data[ i + 1 ],
                        self.data[ i + 2 ]
                    )
                    i += 3
                    c.write_pixel( offset + gf.xy( x, y ), p )

    # =======================================================================

    def _write_from_file(
        self,
        c: gf.canvas,
        offset: gf.xy = gf.xy( 0, 0 )
    ):
        f = open( self.file_name, "rb" )
        f.read( 5 )
        for y in range( self.size.y ):
            for x in range( self.size.x ):

                if self.depth == 0:
                    if ( x % 8 ) == 0:
                        v = f.read( 1 )[ 0 ]
                    c.write_pixel( offset + xy( x, y ), v & 0x01 != 0x00 )
                    v = v >> 1

                elif self.depth == 1:
                    d = f.read( 1 )[ 0 ]
                    r = (( d >> 5 ) & 0x07 ) << 5
                    g = (( d >> 2 ) & 0x07 ) << 5
                    b = (( d >> 0 ) & 0x03 ) << 6
                    c.write_pixel( offset + xy( x, y ), color( r, g, b ) )

                else:
                    d = f.read( 3 )
                    p = color(
                        d[ 0 ],
                        d[ 1 ],
                        d[ 2 ]
                    )
                    c.write_pixel( offset + xy( x, y ), p )
        f.close()

    # =======================================================================

# ===========================================================================
