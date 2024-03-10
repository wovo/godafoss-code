import godafoss as gf
edge = gf.edge()

display = gf.st7789(
    size = gf.xy( 240, 240 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    background = gf.colors.black,
    color_order = "RGB",
    invert = True
)

display.demo()


