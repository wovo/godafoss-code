import godafoss as gf
edge = gf.edge()

pin = edge.pins[ 0 ].as_pin_out()
pw = pin.write

if 0:
 while True:
    pin.write( 0 )
    pin.write( 1 )

if 0:
 while True:
    pw( 0 )
    pw( 1 )
    

import time
import machine
from machine import Pin 
pin = machine.Pin( edge.pins[ 0 ].pin, machine.Pin.OUT)

while True:
    pin.high()
    pin.low()