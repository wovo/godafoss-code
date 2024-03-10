import godafoss as gf
edge = gf.edge()

display = gf.st7735(
    size = gf.xy( 160, 80 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    background = gf.colors.black,
    invert = True,
    #color_order = "RBG",
    swap_xy = True,
    offset = gf.xy( 0, 24 )  
)

display.demo()




