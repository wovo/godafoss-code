import godafoss as gf
edge = gf.edge()

gf.ssd1309_spi(
    size = gf.xy( 128, 64 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    background = False
).demo()
