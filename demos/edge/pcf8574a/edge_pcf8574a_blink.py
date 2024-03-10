import godafoss as gf
edge = gf.edge()

chip = gf.pcf8574a( edge.soft_i2c() )
gf.blink( chip.p0 )