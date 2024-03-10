import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.st7789(      
    size = gf.xy( 320, 240 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    mirror_x = True,
    swap_xy = True
)

display.clear( gf.colors.yellow )
display.flush()

left = display.part( gf.xy( 0, 10 ), gf.xy( 100, 50 ) )
right = display.part( gf.xy( 150, 100 ), gf.xy( 100, 50 ) )
both = gf.all( left, right.inverted() )
both.demo()


