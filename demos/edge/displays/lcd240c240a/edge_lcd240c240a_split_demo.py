import godafoss as gf
edge = gf.edge()

display = gf.lcd240c240a(
    spi = edge.spi( frequency = 20_000_000 ),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight
)

display.clear( gf.colors.yellow )
display.flush()

left = display.part( gf.xy( 10, 10 ), gf.xy( 100, 50 ) )
right = display.part( gf.xy( 100, 100 ), gf.xy( 100, 50 ) )
both = gf.all( left, right.inverted() )
both.demo()


