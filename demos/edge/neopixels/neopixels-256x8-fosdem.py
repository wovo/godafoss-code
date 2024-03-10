import godafoss as gf
import edge

p = gf.ws281x( edge.p5, 256 ).folded( 32, zigzag = True ).xy_swapped()
                               
p.clear()                               
p.write( gf.text( "Fosdem" ) )
p.flush()