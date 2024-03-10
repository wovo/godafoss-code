import godafoss as gf
edge = gf.edge()

amg = gf.amg8831( edge.soft_i2c() )

display = gf.st7735(
    size = gf.xy( 128, 128 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    #backlight = edge.backlight,
    color_order = "BGR",
    swap_xy = True,
    mirror_x = True, 
)

def f( n ):
    n = 4 * ( n - 60 )
    return gf.color( n, n, n )

m = 8

while True:

    data = amg.data()
    display.clear()
    print()

    for x in range( 8 ):
        s = ""
        for y in range( 8 ):
            a = y * 16 + x * 2
            n = data[ a ] + ( data[ a + 1 ] << 8 )
            for i in range( m ):
                for j in range( m ):
                    display.write_pixel( gf.xy( 4 * x + i, 4 * y + j ), f( n ) )
            s += "%8d" % n
        print( s )    
    display.flush()
    gf.sleep_us( 500_000 )
        


