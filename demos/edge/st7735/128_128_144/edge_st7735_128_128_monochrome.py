import godafoss as gf
edge = gf.edge()

display = gf.lcd(
    chip = "st7735",
    size = gf.xy( 128, 128 ),
    spi = edge.spi( frequency = 20_000_000, mechanism = edge.hard ),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
#    color_order = "BGR",
    color_order = None,
    swap_xy = True,
    mirror_x = True,
    mechanism = 0,
)

while False:
    display.clear( True )
    display.flush()
    gf.sleep_us( 500_000 )
    
    display.clear( False )
    display.flush()
    gf.sleep_us( 500_000 )


display.demo()


