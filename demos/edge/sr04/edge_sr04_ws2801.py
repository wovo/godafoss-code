import godafoss as gf
import edge

n_leds = 12

ws = gf.ws2801( edge.p6, edge.p7, n_leds )
sr04 = gf.sr04( edge.p1, edge.p0 )

def bar( n ):
    for i in range( n_leds ):
        ws.write_pixel( gf.xy( n_leds - 1 - i, 0 ),
            gf.colors.red if i >= n else gf.colors.blue // 100 )
    ws.flush()    

while True:
    d = sr04.read()
    if d is not None:
        v = gf.clamp( d // 40, 0, n_leds )
        print( d, v )
        bar ( v )
