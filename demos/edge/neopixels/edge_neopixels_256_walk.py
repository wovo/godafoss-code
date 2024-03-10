import godafoss as gf
import edge

p = gf.ws281x( edge.p5, 256 )
                                
for x in range( p.size.x ):
    p.clear()
    p.write_pixel( gf.xy( x, 0 ), gf.colors.red )
    p.flush()
    gf.sleep_us( 50_000 )