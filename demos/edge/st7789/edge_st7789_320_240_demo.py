import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )
#spi = edge.soft_spi()

display = gf.st7789(      
    size = gf.xy( 320, 240 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = "BGR",
    swap_xy = True
)

display.demo()


