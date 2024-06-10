# ===========================================================================
#
# file     : lcd320c240a.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def lcd320c240a(
    *, 
    spi: gf.spi, 
    data_command: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ],
    chip_select: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None, 
    reset: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None,
    backlight: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None,
    power: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ] = None,
    mechanism: int = 0,
    background: gf.color = gf.colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = gf.orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd320c240a_python", 300 )
    $$insert_image( "lcd320c240a_back", 330 )
    $$add_table( "displays", "lcd320c240a", "lcd320c240a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 2"8                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot, touch interface                           |
    +-------------+---------------------------------------------------------+
    """

    return gf.generic_color_lcd(
    
        # caller-supplied parameters
        spi = spi,
        data_command = data_command,
        chip_select = chip_select,
        reset = reset,
        backlight = backlight,
        power = power,
        mechanism = mechanism,
        background = background,
        monochrome = monochrome,
        invert = invert,
        orientation = orientation,
        
        # display-specific parameters
        size = gf.xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = True,
        swap_xy = True,
        offset = gf.xy( 0, 0 ),
        x_deadband = 0
        
    )

# ===========================================================================
