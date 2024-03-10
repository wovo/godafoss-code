import godafoss as gf
edge = gf.edge()

green = gf.make_pin_out( edge.p0 )
red = gf.make_pin_out( edge.p1 )
yellow = gf.make_pin_out( edge.p2 )
blue = gf.make_pin_out( edge.p3 )
leds = red & green & blue & yellow

gf.blink( leds )

