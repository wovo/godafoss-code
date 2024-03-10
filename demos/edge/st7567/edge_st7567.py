import godafoss as gf
edge = gf.edge()

gf.st7567(
    size = gf.xy( 128, 64 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,    
    background = False
).demo()
