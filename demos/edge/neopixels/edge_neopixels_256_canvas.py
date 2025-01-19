import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 256 ).folded( 32 ).xy_swapped()
                                
p.demo()