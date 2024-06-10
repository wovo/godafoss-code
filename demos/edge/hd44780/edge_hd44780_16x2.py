import godafoss as gf
edge = gf.edge()

d = gf.hd44780(
    size = gf.xy( 16, 2 ),
    data = gf.make_port_out( edge.p4, edge.p5, edge.p6, edge.p7 ),
    rs = edge.p0,
    rw = edge.p1,
    e = edge.p2,
    backlight = edge.p3
)

d.write( "\fHello brave new\nworld." )