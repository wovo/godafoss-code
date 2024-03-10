# ===========================================================================
#
# file     : text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class text( gf.shape ):

    def __init__(
        self,
        text: str,
        font: gf.font = None
    ):
        self._text = text
        self._font = font
        if self._font == None:
            # avoid draging in font_default.read()
            self._font = gf.font_default()
            self.size = gf.xy( len( self._text ) * 8, 8 )
        else:
            self.size = gf.xy(
                sum( [ self._font.read( c ).size.x for c in text ] ),
                self._font.size.y
            )
        gf.shape.__init__( self )

    def write(
        self,
        sheet,
        offset: gf.xy = gf.xy( 0, 0 ),
        ink: [ gf.color, bool, None ] = True
    ):
        x_offset_in_text = 0
        y_offset = 0
        for c in self._text:

            if c == '\n':
                x_offset_in_text = 0
                y_offset += self._font.size.y

                # quit when below the sheet
                if y_offset >= sheet.size.y:
                    return

                continue

            glyph = self._font.read( c )
            x_offset_in_sheet = offset.x + x_offset_in_text

            # skip when beyond the right side of the sheet
            if (
                # skip when before the left side of the sheet
                ( x_offset_in_sheet + glyph.size.x >= 0 )

                # skip when beyond the right side of the sheet
                and ( x_offset_in_sheet < sheet.size.x )
            ):
                glyph.write(
                    sheet,
                    offset + gf.xy( x_offset_in_text, y_offset ),
                    ink
                )

            x_offset_in_text += glyph.size.x




# ===========================================================================

