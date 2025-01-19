import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 64 ).folded( 8, zigzag = True ).xy_swapped()
          
while True:
 p.clear()                               
 p.write( gf.text( "F" ) )
 p.flush() 
 gf.sleep_us( 500_000 )

 
 p.clear()
 p.write( gf.text( "o" ) )
 p.flush()
 gf.sleep_us( 500_000 )
