# ===========================================================================
#
# file     : glyph.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2022
# license  : MIT license, see license variable in the code
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================

import sys
from PIL import Image


# ===========================================================================

def make_glyph( input_file, output_name, x_size, y_size ):

    im = Image.open( input_file )
    
    if x_size != 0:
        if y_size == 0:
            y_size = im.size[ 1 ] * x_size // im.size[ 0 ]
            
    if y_size != 0:
        if x_size == 0:
            x_size = im.size[ 0 ] * y_size // im.size[ 1 ]
            
    if x_size == 0:
        x_size, y_size = im.size

    im = im.resize( ( x_size, y_size ) )    
    if not isinstance( im.getpixel( ( 0, 0 ) ), int ):
        print( "The input must be a b/w file." )
                       
    b = 0
    n = 0
    data = []
    for y in range( y_size ):
        s = ""
        for x in range( x_size ):
            n += 1
            c = im.getpixel( ( x, y ) )
            b = b >> 1
            if c:
                b |= 0x80
                s += " "
            else:
                s += "O"                
            if ( n % 8 == 7 ) or ( n + 1 == x * y ):
                data.append( b )
                b = 0
        if 1: print( "%2d|" % y + s + "|" )
    
    f = open( output_name + ".py", "w" )
    
    f.write( "from godafoss import xy, glyph\n" )
    f.write( "\n" )
    f.write( "class %s( glyph ):\n" % output_name )
    f.write( "    \"\"\"\n" );
    f.write( "    image generated from %s\n" % input_file )
    f.write( "    size %d * %d\n" % ( x_size, y_size ) ) 
    f.write( "    \"\"\"\n" );
    f.write( "\n" )
    f.write( "    def __init__( self ) -> None:\n" )
    f.write( "        glyph.__init__( self, xy( %d, %d ) )\n" 
        % ( x_size, y_size ) )
    f.write( "        self.data = bytes( [\n" )
    s = ""
    for i in range( len( data ) ):
       s += "%d," % data[ i ]
       if ( len( s ) > 50 ) or ( i + 1 == len( data )):
           f.write( "            %s\n" % s )
           s = ""
    f.write( "        ] )\n" )   
    f.write( "\n" )       
    f.write( "    def read( self, location: xy ) -> color:\n" ) 
    f.write( "        n = location.x + location.y * self.size.x\n" )
    f.write( "        b = self.data[ n // 8 ] & ( 0x1 << ( n % 8 ))\n" )
    f.write( "        return b != 0\n" )  
        
    f.close()
    im.close()

    
# ===========================================================================

def run( args ):
    if len( args ) < 3:
        print( "usage:" )
        print( "    glyph input_file output [x_size] [y_size]" )
        print( "" )
        print( "input_file:  image file, must be a b/w acceptable to PIL.Image.open()" )
        print( "output:      output file name (.py will be appended) and python image class name" )
        print( "x_size:      x_size of the written image. default: taken from input." )
        print( "y_size:      y_size of the written image. default: taken from input." )
        print( " " )
        print( "When either the x_size is specified but the y_size is not or is 0," )
        print( "or the y_size is omitted, the aspect ratio is maintained." )
        return
                  
    make_glyph( 
        args[ 1 ], 
        args[ 2 ], 
        int( args[ 4 ] ) if len( args ) > 4 else 0,
        int( args[ 5 ] ) if len( args ) > 5 else 0
    )        

        
# ===========================================================================

if __name__ == "__main__":
    run( sys.argv )

    
# ===========================================================================
  