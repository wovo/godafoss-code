import godafoss as gf
edge = gf.edge()

spi = edge.spi() # hard_spi( 1, 10_000_000 )

display = gf.st7789(
    size = gf.xy( 240, 320 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    #background = gf.colors.black,
    #invert = False,
    #order = "RBG",
    #xy_swap = True,
    #x_reverse = True,
    #offset = gf.xy( 0, 0 ),
    #x_deadband = 0
)

touch = gf.xpt2046(
    spi = spi,
    cs = edge.p7,
    size = display.size
)

display.clear( gf.colors.blue )
display.flush()
while True:
    t_adc = touch.touch_adcs()
    t_fractions = touch.touch_fractions()
    if t_fractions != None:
        t = touch.touch_xy( display.size )
        print( t_fractions, t )
        display.write( gf.circle( 10 ), t)
        display.flush()
        gf.sleep_us( 100_000 )

display.clear()
gf.line( gf.xy( 100, 100 ) ).write( display )
gf.text( "XXXXX" ).write( display )
display.flush()
display.demo()


