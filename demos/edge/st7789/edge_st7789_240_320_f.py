import godafoss as gf
import edge

spi = edge.hard_spi( 1, 20_000_000 )
# spi = edge.soft_spi()

display = gf.st7789(
    size = gf.xy( 240, 320 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    #background = gf.colors.black,
    #invert = False,
    order = "BRG",
    #xy_swap = True,
    #x_reverse = True,
    #offset = gf.xy( 0, 0 ),
    #x_deadband = 0
)

#display.demo()

display.clear( gf.colors.red )
# display.clear()
f = gf.ggf( "f" )
f.write( display )
display.flush()


