import godafoss as gf

spi = gf.spi( 
    sck = 2,
    mosi = 3,
    miso = 4,
    mechanism = gf.spi.soft
)

print( "luatos_esp32c3 + air101-lcd demo lcd" )

display = gf.st7735(
    size = gf.xy( 160,80 ),
    spi = spi,
    data_command = 6,
    chip_select = 7,
    reset = 10,
    backlight = 11,
    color_order = "BGR",
    swap_xy = True,
    mirror_x = True,
    offset = gf.xy( 0, 24 )
)

display.demo()


