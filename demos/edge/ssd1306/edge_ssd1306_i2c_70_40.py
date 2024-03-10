import godafoss as gf
edge = gf.edge()

gf.ssd1306_i2c(
    gf.xy( 70, 40 ),
    edge.soft_i2c(),
    background = False
).demo()
