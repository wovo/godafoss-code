import godafoss as gf
edge = gf.edge()

chip = gf.pcf8575( edge.soft_i2c() )
gf.kitt( chip.inverted() )