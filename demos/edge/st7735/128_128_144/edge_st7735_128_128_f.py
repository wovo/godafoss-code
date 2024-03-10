import godafoss as gf
edge = gf.edge()

display = gf.lcd(
    chip = "st7735",
    size = gf.xy( 128, 128 ),
    spi = edge.hard_spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = "BGR",
    swap_xy = True,
    mirror_x = True, 
)

display.clear( gf.colors.red )
f = gf.ggf( "f" )
f.write( display )
display.flush()
