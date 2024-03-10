import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.st7789(
    size = gf.xy( 240, 240 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    background = gf.colors.black,
    color_order = None,
    invert = True,
    mechanism = 2
)

display.demo()


