import godafoss as gf
edge = gf.edge()

display = gf.tm1640(
    size = gf.xy( 16, 8 ),
    background = gf.colors.black,
    sclk = edge.spi_sck,
    din = edge.spi_mosi,
    brightness = 0
)

display.demo()
