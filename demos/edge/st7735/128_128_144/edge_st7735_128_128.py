import godafoss as gf
edge = gf.edge()

display = gf.st7735(
    size = gf.xy( 128, 128 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = "BGR",
    swap_xy = True,
    mirror_x = True, 
)

display.demo()


