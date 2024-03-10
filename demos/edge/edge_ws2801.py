import godafoss as gf
import edge

ws = gf.ws2801( edge.p6, edge.p7, 8 )
#ws.demo()
ws.write_pixel( gf.xy( 0, 0 ), gf.colors.black )
ws.write_pixel( gf.xy( 1, 0 ), gf.colors.red )
ws.write_pixel( gf.xy( 2, 0 ), gf.colors.green )
ws.write_pixel( gf.xy( 3, 0 ), gf.colors.blue )
ws.write_pixel( gf.xy( 4, 0 ), gf.colors.white )
ws.flush()
# ws.demo()