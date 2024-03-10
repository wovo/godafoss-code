import godafoss as gf
edge = gf.edge()

amg = gf.amg8831( edge.soft_i2c() )

data = amg.data()

for x in range( 8 ):
    s = ""
    for y in range( 8 ):
        a = y * 16 + x * 2
        n = data[ a ] + ( data[ a + 1 ] << 8 )
        s += "%8d" % n
    print( s )
        


