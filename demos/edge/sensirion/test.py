import godafoss as gf
edge = gf.edge()
s = gf.slf3s_1300f( edge.soft_i2c( frequency = 100_000 ) )

#s.start()
#print( s.flow() )
#s.stop()

s.demo()

