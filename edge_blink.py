import godafoss as gf
gf.gpio_blinka()
edge = gf.edge()
gf.blink( edge.pins[ 0 ].pin )
