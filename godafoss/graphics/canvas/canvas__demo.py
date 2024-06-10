# ===========================================================================
#
# file     : canvas__demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
from random import randint


# ===========================================================================

def canvas__demo(
    s: gf.canvas,
    iterations = None
):
    print( "canvas demos", s.size )
    pixels = s.size.x * s.size.y

    for iteration in gf.repeater( iterations ):

        if iteration == 0:
            gf.report_memory_and_time()

        if s.is_color:
            gf.canvas_demo_colors( s, iterations = 1 )
            if pixels > 256:
                gf.canvas_demo_color_gradients( s, iterations = 1 )

        if pixels <= 256:
            gf.canvas_demo_blink( s, iterations = 3 )
            gf.canvas_demo_filling( s, iterations = 1 )

        else:
            gf.canvas_demo_lines( s, iterations = 1 )
            gf.canvas_demo_rectangles( s, iterations = 1 )
            gf.canvas_demo_circles( s, iterations = 1 )
            gf.canvas_demo_text( s, iterations = 1 )

        if 0: canvas_demo_scrolling_text(
            s,
            "Hello fantastic brave new world!\nusing Godafoss",
            iterations = 1
        )

        if iteration == 0:
            gf.report_memory_and_time()

# ===========================================================================
