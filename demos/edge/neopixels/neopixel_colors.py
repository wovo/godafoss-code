import godafoss as gf
import edge

neopixels = gf.ws281x( edge.p5, 300 )
neopixels.demo_color_wheel()
