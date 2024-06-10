import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.st7789(
    size = gf.xy( 240, 320 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = "BGR",
    mirror_x = True,
    mirror_y = True,
)

display.demo()