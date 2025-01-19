import godafoss as gf
edge = gf.edge()

n = gf.ws281x( edge.neopixel_data, 64 )
n.demo()