import godafoss as gf
import machine

reset = gf.gpio_out( 16 )
reset.write( 1 )

i2c = machine.SoftI2C(
        scl = machine.Pin( 15, machine.Pin.OUT ),
        sda = machine.Pin(  4, machine.Pin.OUT )
    )

oled = gf.ssd1306_i2c(
    gf.xy( 128, 64 ),
    i2c
)

#import LoRaDuplexCallback
#import LoRaPingPong
#import LoRaSender
from examples import LoRaSender
from examples import LoRaReceiver

from config import *
from machine import Pin, SoftSPI, SPI
from sx127x import SX127x

device_spi = SoftSPI(baudrate = 10000000, 
        #polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)

oled.clear()
oled.write( "LoRa Sender" )
oled.flush()

counter = 0
while True:
        payload = 'Hello ({0})'.format(counter)
        oled.clear()
        oled.write( "{0} \nRSSI: {1}".format(payload, lora.packet_rssi()) )
        oled.flush()
        
        print( payload )
        lora.println(payload)

        counter += 1
        gf.sleep_us( 5_000_000 )
