import godafoss as gf
import edge

a = gf.xy( 2, 2 )
b = gf.xy( 15, 5 )

tm = gf.tm1640(
    size = gf.xy( 16, 8 ),
    background = gf.colors.black,
    sclk = edge.p0,
    din = edge.p1
)


tm.clear()
tm.draw_line( a, b )
tm.flush()