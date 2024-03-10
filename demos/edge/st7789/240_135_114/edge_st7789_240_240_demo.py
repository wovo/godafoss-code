import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.st7789(
    size = gf.xy( 240, 135 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = "RGB",
    invert = True,
    swap_xy = True,    
    mirror_x = True,
    offset = gf.xy( 40, 53 )
)

display.demo()