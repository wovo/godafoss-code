import godafoss as gf
import edge

p = gf.ws281x( edge.p5, 64 ).folded( 8, zigzag = True ).xy_swapped()
                               
p.clear()                               
p.write( gf.text( "F" ) )
p.flush()