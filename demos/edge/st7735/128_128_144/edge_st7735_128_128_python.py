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
    color_order = "RBG",
    swap_xy = True,
    mirror_x = True, 
)

python = gf.ggf( "micropython_128_128" )
display.write( python )
display.flush()


