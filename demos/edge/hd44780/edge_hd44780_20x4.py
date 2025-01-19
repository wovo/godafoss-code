import godafoss as gf
edge = gf.edge()

size = gf.xy( 20, 4 )
data = gf.make_port_out( edge.p4, edge.p5, edge.p6, edge.p7 )

d = gf.hd44780(
    size = size, # gf.xy( 20, 4 ),
    data = data, # gf.port_out( edge.p4, edge.p5, edge.p6, edge.p7 ),
    rs = edge.p0,
    rw = edge.p1,
    e = edge.p2,
    backlight = edge.p3
)

print( "x" )

d.write( "\fHello brave new\nworld." )

print( "y" )