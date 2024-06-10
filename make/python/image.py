# ===========================================================================
#
# file     : image.py
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

def make_image( input_file, output_name, depth, x_size, y_size ):
    if not depth in [ 1, 8, 24 ]:
        print( "depth must be 1, 8 or 24" )
        return

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
    
    data = []
    if depth == 1:
        im = im.convert( 'L' ) # greyscale
        
        average = 0
        for y in range( y_size ):
            for x in range( x_size ):
                average += im.getpixel( ( x, y ) )
        average = average / ( y_size * x_size )
                
        b = 0
        n = 0
        for y in range( y_size ):
            s = ""
            for x in range( x_size ):
                n += 1
                c = im.getpixel( ( x, y ) )
                b = b >> 1
                if c >= average: 
                    b |= 0x80
                    s += " "
                else:
                    s += "O"                
                if ( n % 8 == 7 ) or ( n + 1 == x * y ):
                    data.append( b )
                    b = 0
            if 1: print( "%2d|" % y + s + "|" )
                
    elif depth == 8:
        pass
    else:        
        pass
    
    f = open( output_name + ".py", "w" )
    
    f.write( "from godafoss import xy, color, colors, image\n" )
    f.write( "\n" )
    f.write( "class %s( gf.image ):\n" % output_name )
    f.write( "    \"\"\"\n" );
    f.write( "    image generated from %s\n" % input_file )
    f.write( "    size %d * %d\n" % ( x_size, y_size ) )
    f.write( "    color depth %d\n" % depth ) 
    f.write( "    \"\"\"\n" );
    f.write( "\n" )
    f.write( "    def __init__( self ) -> None:\n" )
    f.write( "        image.__init__( self, xy( %d, %d ) )\n" 
        % ( x_size, y_size ) )
    f.write( "        self.data = bytes(\n" )
    s = ""
    for i in range( len( data ) ):
       s += "\\0x%02x" % data[ i ]
       if ( len( s ) > 50 ) or ( i + 1 == len( data )):
           f.write( "            \"%s\"\n" % s )
           s = ""
    f.write( "        )\n" )   
    f.write( "\n" )       
    f.write( "    def read( location: xy ) -> color:\n" ) 
    f.write( "        n = xy.x + xy.y * self.size.x\n" )
    if depth == 1:
        f.write( "        b = self.data[ n % 8 ] & ( 0x1 << ( n % 8 ))\n" )
        f.write( "        return colors.black if b == 0 else colors.white\n" )
    elif depth == 8:
        f.write( "        return self.data\n" )
    else:
        f.write( "        return self.data\n" )    
        
    f.close()
    im.close()

    
# ===========================================================================

def run( args ):
    if len( args ) < 3:
        print( "usage:" )
        print( "    image input_file output [depth] [x_size] [y_size]" )
        print( "" )
        print( "input_file:  image file, must be acceptable to PIL.Image.open()" )
        print( "output:      output file name (.py will be appended) and python image class name" )
        print( "depth:       color depth in bits, must be 1, 8 or 24. default is 8" )
        print( "x_size:      x_size of the written image. default: taken from input." )
        print( "y_size:      y_size of the written image. default: taken from input." )
        print( " " )
        print( "When either the x_size is specified but the y_size is not or is 0," )
        print( "or the y_size is omitted, the aspect ratio is maintained." )
        return
                  
    make_image( 
        args[ 1 ], 
        args[ 2 ], 
        int( args[ 3 ] ) if len( args ) > 3 else 8,
        int( args[ 4 ] ) if len( args ) > 4 else 0,
        int( args[ 5 ] ) if len( args ) > 5 else 0
    )        

        
# ===========================================================================

if __name__ == "__main__":
    run( sys.argv )

    
# ===========================================================================
  