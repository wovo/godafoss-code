import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.glcd(      
    size = gf.xy( 320, 240 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    mirror_x = True,
    swap_xy = True
)

display.demo()


