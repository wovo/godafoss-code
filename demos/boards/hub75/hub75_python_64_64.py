import godafoss as gf

display = gf.hub75(
    size = gf.xy( 128, 32 ),
    r1_b2 = 2,
    a_e = 10,
    clk_lat_oe = 26,
    frequency = 10_000_000
).folded( 2 )

python = gf.ggf( "python_64_64.ggf" )
display.write( python )
display.flush()


