import godafoss as gf
edge = gf.edge()

display = gf.max7219(
    n = 8,
    spi = edge.spi(),
    chip_select = edge.chip_select,
    background = False,
    brightness = 0
).folded( 2 )
display.demo()


