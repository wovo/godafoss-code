import godafoss as gf
edge = gf.edge()

d = gf.hd44780_pcf8574a(
    size = gf.xy( 16, 2 ),
    bus = edge.soft_i2c()  
)

d.write( "\fHello brave new\nworld!" )