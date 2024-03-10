# ===========================================================================
#
# file     : ggf.py
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
#import numpy


# ===========================================================================

def make_ggf( 
    input_file, 
    output_name, 
    depth, 
    x_size, 
    y_size 
):
    if not depth in [ 1, 8, 24 ]:
        print( "depth must be 1, 8 or 24 (not %d)" % depth )
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
            if 0: print( "%2d|" % y + s + "|" )
                
    elif depth == 8:
        pass
        
    else:        
        pass
        
    #im_matrix = np.array(im)         
    
    if not output_name.endswith( ".ggf" ):
        output_name += ".ggf"
    f = open( output_name, "wb" )
    f.write( bytes( [ 0xA6 ] ) )
    f.write( bytes( [ { 1:0, 8:1, 24:2 }[ depth ] ] ) )
    f.write( bytes( [ x_size // 256, x_size % 256 ] ) )
    f.write( bytes( [ y_size // 256, y_size % 256 ] ) )
    v = 0
    m = 1
    for y in range( y_size ):
        for x in range( x_size ):
            p = im.getpixel( ( x, y ) )
            if depth == 1:
                if p > 127:
                    v |= m    
                m = m << 1  
                if ( ( x % 8 ) == 7 ) or ( x == ( x_size - 1 ) ):
                    f.write( bytes( [ v ] ) )
                    v = 0
                    m = 1

            elif depth == 8:
                r = ( p[ 0 ] >> 5 ) & 0x07
                g = ( p[ 1 ] >> 5 ) & 0x07
                b = ( p[ 2 ] >> 6 ) & 0x03
                rgb = ( r << 5 ) | ( g << 2 ) | ( b << 0 )
                f.write( bytes( [ rgb ] ) )
                
            else:
                f.write( bytes( p ) )          
        
    f.close()
    
# ===========================================================================

def show_ggf( file_name ):
    if not file_name.endswith( ".ggf" ):
        file_name += ".ggf"
    f = open( file_name, "rb" )
    
    x = f.read( 1 )[ 0 ]
    if x != 0xA6:
        print( "file %s first byte %02X, should be 0xA6" 
            % ( file_name, x ) )
        return
        
    depth = f.read( 1 )[ 0 ]    
    if not depth in [ 0, 1, 2 ]:
        print( "file %s depth byte %d, should be 0,1,2" 
            % ( file_name, depth ) )
        return    
        
    s = f.read( 2 )
    x_size = s[ 0 ] * 256 + s[ 1 ]
    s = f.read( 2 )
    y_size = s[ 0 ] * 256 + s[ 1 ]
    
    print( "size (%d,%d) format %d" % ( x_size, y_size, depth ) )
    img = Image.new( 'RGB', (x_size, y_size), color = 'red' )
    
    for y in range( y_size ):
        for x in range( x_size ):
        
            if depth == 0:
                if ( x % 8 ) == 0:
                    v = f.read( 1 )[ 0 ]
                c = 0xFF if v & 0x01 else 0x00
                img.putpixel( ( x, y ), ( c, c, c ) )  
                
            elif depth == 1:    
                c = f.read( 1 )[ 0 ]
                r = ( c >> 5 ) & 0x07
                g = ( c >> 2 ) & 0x07
                b = ( c >> 0 ) & 0x03
                img.putpixel( ( x, y ), ( r << 5, g << 5, b << 6 ) )
                
            else:
                c = tuple( f.read( 3 ) )
                #a, b, c = c
                # c = ( a & 0xE0, b & 0xE0, c & 0xC0 )
                #c = ( 255, b, c )
                img.putpixel( ( x, y ), c )
    
    img.show()
    f.close()

# ===========================================================================

def run( args ):
    if len( args ) < 2:
        print( "usage:" )
        print( "    ggf input_file " )
        print( "" )
        print( "Open the input file (.ggf appended when needed) in the default image viewer application" )
        print( "" )
        print( "usage:" )
        print( "    ggf input_file output [depth] [x_size] [y_size]" )
        print( "" )
        print( "input_file:  image file, must be acceptable to PIL.Image.open()" )
        print( "output:      output file name (.ggf will be appended)" )
        print( "depth:       color depth in bits, must be 1, 8 or 24. default is 24" )
        print( "x_size:      x_size of the written image. default: taken from input." )
        print( "y_size:      y_size of the written image. default: taken from input." )
        print( " " )
        print( "When either the x_size is specified but the y_size is not or is 0," )
        print( "or the y_size is omitted, the aspect ratio is maintained." )
        return
            
    if len( args ) == 2:
        show_ggf( args[ 1 ] )
        
    else:           
        make_ggf( 
            args[ 1 ], 
            args[ 2 ], 
            int( args[ 3 ] ) if len( args ) > 3 else 24,
            int( args[ 4 ] ) if len( args ) > 4 else 0,
            int( args[ 5 ] ) if len( args ) > 5 else 0
        )        

# ===========================================================================

if __name__ == "__main__":
    run( sys.argv )

# ===========================================================================
  