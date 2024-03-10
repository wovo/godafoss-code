import godafoss as gf
import edge

p = gf.ws281x( edge.p5, 300 )
                                
p.demo_color_wheel( dim = 1, delay = 100 )  