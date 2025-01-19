import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 256 )
                                
p.demo_color_wheel( dim = 30 )   