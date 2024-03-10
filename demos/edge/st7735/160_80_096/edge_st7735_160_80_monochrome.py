import godafoss as gf
edge = gf.edge()

display = gf.st7735(
    size = gf.xy( 160,80 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = None,
    swap_xy = True,
    mirror_x = True,
    offset = gf.xy( 0, 24 )
)

while False:
    display.clear( True )
    display.flush()
    gf.sleep_us( 500_000 )
    
    display.clear( False )
    display.flush()
    gf.sleep_us( 500_000 )


display.demo()


