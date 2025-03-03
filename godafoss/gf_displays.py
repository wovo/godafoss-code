# ===========================================================================
#
# file     : displays.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from godafoss import *

#$$document( 0 )


# ===========================================================================

def oled128m32a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "oled128m32a_python", 300 )
    $$insert_image( "oled128m32a_back", 330 )
    $$add_table( "displays", "oled128m32a", "oled_128m32a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 2"8                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot, touch interface                           |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        size = xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = True,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def oled128m64a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "oled128m32a_python", 300 )
    $$insert_image( "oled128m32a_back", 330 )
    $$add_table( "displays", "oled128m32a", "oled_128m32a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 2"8                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot, touch interface                           |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        size = xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = True,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd128c128a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd128c128a_python", 300 )
    $$insert_image( "lcd128c128a_back", 330 )
    $$add_table( "displays", "lcd128c128a", "lcd128c128a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 128 x 128 RGB LCD 1"44                                  |
    +-------------+---------------------------------------------------------+
    | controller  | ST7735                                                  |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        size = xy( 128, 128 ),
        color_order = "BGR",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd128c128b(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd128c128b_python", 300 )
    $$insert_image( "lcd128c128b_back", 330 )
    $$add_table( "displays", "lcd128c128b", "lcd128c128b_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 128 x 128 RGB LCD 2"8                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot, touch interface                           |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        size = xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = True,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd160c80a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd160c80a_python", 300 )
    $$insert_image( "lcd160c80a_back", 330 )
    $$add_table( "displays", "lcd160c80a", "lcd160c80a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 160 x 80 RGB LCD 0"96                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7735S                                                 |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        invert = not invert,
        orientation = orientation,
        
        # display-specific parameters
        size = xy( 160, 80 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = False,
        swap_xy = True,
        offset = xy( 0, 24 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd160c128a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
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

    return generic_color_lcd(
    
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
        size = xy( 160, 128 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd240c135a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd240c135a_python", 300 )
    $$insert_image( "lcd240c135a_back", 330 )
    $$add_table( "displays", "lcd240c135a", "lcd240c135a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 1"14                                  |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        invert = not invert,
        orientation = orientation,
        
        # display-specific parameters
        size = xy( 240, 135 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = [
            xy( 40, 53 ),
            xy( 40, 53 ),
            xy( 40, 52 ),
            xy( 40, 52 ),
        ],
        x_deadband = 0
        
    )


# ===========================================================================

def lcd240c240a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd240c240a_python", 300 )
    $$insert_image( "lcd240c240a_back", 330 )
    $$add_table( "displays", "lcd240c240a", "lcd240c240a_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 240 RGB LCD 1"3                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+

    """

    return generic_color_lcd(
    
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
        invert = not invert,
        orientation = orientation,
        
        # display-specific parameters
        size = xy( 240, 240 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd320c240a(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
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

    return generic_color_lcd(
    
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
        size = xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = False,
        mirror_y = True,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd320c240b(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd320c240b_python", 300 )
    $$insert_image( "lcd320c240b_back", 330 )
    $$add_table( "displays", "lcd320c240b", "lcd320c240b_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 2"2                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    | extras      | SD card slot                                            |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        size = xy( 320, 240 ),
        color_order = "BGR",
        mirror_x = True,
        mirror_y = True,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

def lcd320c240c(
    *, 
    spi: spi, 
    data_command: [ int, pin_out, pin_in_out, pin_oc ],
    chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
    reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
    backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
    power: [ int, pin_out, pin_in_out, pin_oc ] = None,
    mechanism: int = 0,
    background: color = colors.black, 
    monochrome: bool = False,
    invert: bool = False,
    orientation: int = orientation.north 
) -> "generic_color_lcd":

    """
    $$insert_image( "lcd320c240c_python", 300 )
    $$insert_image( "lcd320c240c_back", 330 )
    $$add_table( "displays", "lcd320c240c", "lcd320c240c_python" )     
    
    +-------------+---------------------------------------------------------+
    | size        | 240 x 320 RGB LCD 2"0                                   |
    +-------------+---------------------------------------------------------+
    | controller  | ST7789                                                  |
    +-------------+---------------------------------------------------------+
    """

    return generic_color_lcd(
    
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
        invert = not invert,
        orientation = orientation,
        
        # display-specific parameters
        size = xy( 320, 240 ),
        color_order = "RGB",
        mirror_x = True,
        mirror_y = False,
        swap_xy = True,
        offset = xy( 0, 0 ),
        x_deadband = 0
        
    )


# ===========================================================================

