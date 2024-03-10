import godafoss as gf
edge = gf.edge()

chip = gf.mcp23017( edge.soft_i2c() )
gf.kitt( chip.inverted() )