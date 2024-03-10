# ===========================================================================
#
# file     : gf_canvas_demos.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains various sheet demos
#
# ===========================================================================

from random import randint

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_line import *
from godafoss.gf_rectangle import *
from godafoss.gf_circle import *
from godafoss.gf_text import *


# ===========================================================================

def cnvas_demo_lines( s : canvas, iterations = None, frame = True ):

    print( "canvas demo lines", s.size )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for _ in range( 0, 20 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            s.write( line( end - start ) @ start )
            s.flush()
            sleep_us( 100_000 )
            
        sleep_us( 2_000_000 )
        
# ===========================================================================

def canvas_demo_rectangles( s : sheet, iterations = None, frame = True ):

    print( "canvas demo rectangles", s.size )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for dummy in range( 0, 10 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( rectangle( end - start ) @ start )
            s.flush()
            sleep_us( 100_000 )            
            
        sleep_us( 2_000_000 )        
        

# ===========================================================================

def canvas_demo_circles( s : sheet, iterations = None, frame = True ):

    print( "canvas demo circles", s.size )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for _ in range( 0, 20 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            radius = randint( 0, min( s.size.x, s.size.y ) // 2 )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( circle( radius ) @ start )
            s.flush()
            sleep_us( 100_000 )            
            
        sleep_us( 2_000_000 )
        

# ===========================================================================

def canvas_demo_text( s : sheet, iterations = None, frame = True ):

    print( "canvas demo text", s.size )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            sleep_us( 500_000 )
        
        s.write( text( "Hello world" ) @ xy( 1, 1 ) )
        s.flush()
        sleep_us( 500_000 )
        
        s.write( text( "Micropython" ) @ xy( 1, 9 ) )
        s.flush()
        sleep_us( 500_000 )
        
        s.write( text(  "+ Godafoss" ) @ xy( 1, 17 ) )
        s.flush()
        sleep_us( 2_000_000 )
        
# ===========================================================================

def canvas_demo_scrolling_text(
    s: sheet,
    t: [ str, text ],
    scroll_pause: int =  100,
    end_pause: int = 1_000_000,
    iterations = None, 
):
    print( "canvas demo scrolling text", s.size )
        
    if isinstance( t, str ):
        t = text( t )
        
    for _ in repeater( iterations ):
        for x in range( 0, t.size.x - s.size.x ):
            s.clear()
            s.write( t @ xy( - x, 0 ) )
            s.flush()
            sleep_us( scroll_pause )
        sleep_us( end_pause )

# ===========================================================================

def canvas_demo( 
    s: sheet,
    iterations = None
):
    for _ in repeater( iterations ):         
        canvas_demo_lines( s, iterations = 1 )
        canvas_demo_rectangles( s, iterations = 1 )
        canvas_demo_circles( s, iterations = 1 )
        canvas_demo_text( s, iterations = 1 )
        canvas_demo_scrolling_text(
            s,
            "Hello fantastic brave new world!\nusing Godafoss",
            iterations = 1
        )
    

# ===========================================================================
