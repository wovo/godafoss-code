import godafoss as gf
edge = gf.edge()

size = gf.xy( 20, 4 )
data = gf.port_out( edge.pins[ 4 : 8 ] )

d = gf.hd44780(
    size = size,
    data = data,
    rs =  edge.pins[ 0 ],
    rw =  edge.pins[ 1 ],
    e =  edge.pins[ 2 ],
    backlight =  edge.pins[ 3 ]
)

print( "x" )

d.write( "\fHello brave new\nworld." )

print( "y" )