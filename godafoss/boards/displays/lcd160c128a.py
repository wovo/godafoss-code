# ===========================================================================
#
# file     : lcd160c128a.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def lcd160c128a(
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
    $$insert_image( "lcd160c128a_python", 300 )
    $$insert_image( "lcd160c128a_back", 330 )
    $$add_table( "displays", "lcd160c128a", "lcd160c128a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 160 x 128 RGB LCD 1"8                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot                                            |
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
        size = gf.xy( 160, 128 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = gf.xy( 0, 0 ),
        x_deadband = 0
        
    )

# ===========================================================================
