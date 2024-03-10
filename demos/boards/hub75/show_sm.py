import rp2
for i in range( 2 ):
    p = rp2.PIO( i ) 
    print( i, p )
    for n in range( 4 ):
        m = p.state_machine( n )
        print( n, m, m.active() )
        
rp2.PIO(0).state_machine(0).active(0)        