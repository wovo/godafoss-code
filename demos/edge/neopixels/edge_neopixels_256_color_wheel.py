import godafoss as gf
import edge

p = gf.ws281x( edge.p5, 256 )
                                
p.demo_color_wheel( dim = 30 )   