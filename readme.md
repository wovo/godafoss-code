This is the source repository for 
[godafoss](https://https://wovo.github.io/godafoss), 
a micro-python library.

To work on the sources, clone this repository 
(wovo/godafoss-code, not wovo/godafoss)
and copy the godafoss directory to your MicroPython device.

TODO
====

- disinguish e-ink from other displays
- separate demo for e-ink
- use built-ins for rectangle, circle, etc, check badger2040
- badger gray-scale: remove or include??
- shared copyright, mention elsewhere???
- badge demo for e-inks!
- more fonts?
- badger demo, incl switching -> display QR
- e-ink has some ghosting...
- write (text) framed, centered, bold, enlarged
- maybe framed_write()
- rotate etc. voor die badge

- test board for pin directions using resistors
- blink fast all same results on pico 2?
- test blinka & direct on pi
- https://abyz.me.uk/rpi/pigpio/examples.html#Python%20code

- analog demo ala input pin
- way to run demos/edge/edge_blink.py directly from dos prompt
- hd44780
- bus.py i2c & spi & neopixels & lcd base abstractions
- use time asbstraction (one) ?
- check pullup handling
- test coverage
- auto-detect usb serial on Linux

- cleanup files before ports.py

- avoid lambda and local classes because they are created in RAM?
- subrange of ports?

- repeater, pulse etc. should use await() which can take a moment or a duration
- deprecate esp8266
- write to 2 ports
- blink & pulse on port

lcd_spi_cd.py should be spi_cd.py

where does sleep() come from??

xy - is an immutable...
xyz.within

for images:
https://github.com/peterhinch/micropython-samples/blob/master/SERIALISATION.md

mcp2515

pass pullup parameters
gpio plaatje
$$ref() enzo moeten inline zijn, andere structuur (command class)
pins: invert the description, refer to links
- pin_in
- pin_out
- pin_in_out
- pulse + plaatje
- refer to $pulse (=function)

http://www.jczn1688.com/zlxz
https://registry.platformio.org/libraries/rzeldent/esp32_smartdisplay

https://en.wikipedia.org/wiki/ESP32
https://en.wikipedia.org/wiki/ESP8266
https://forum.micropython.org/viewtopic.php?t=1747
https://en.wikipedia.org/wiki/RP2040
https://github.com/OkuboHeavyIndustries?tab=repositories - 128x64 grpahics

If using Thonny IDE, in the Tools -> Manage Packages menu, search for "MicroPython_CAN_BUS_MCP2515" and install

- lcd has too many parameters
- sort lcds and boards alphabetically before inserting
- mention using a powered hub for 4.1
- make/build and make/load commands
- iets weirds met links, maak er een $$class() van
- generic_lcd afmaken
- more lcds
https://luma-lcd.readthedocs.io/en/latest/
https://www.espruino.com/Graphics?print
https://github.com/rm-hull/luma.lcd/blob/master/doc/python-usage.rst

lcd240c320a
oled128m64a
epaper240m320a

blinka: pin_in_out pin_in pin_oc spi i2c

reversie game with touch

https://abyz.me.uk/rpi/pigpio/python.html
check https://github.com/russhughes/gc9a01py for fonts
sx127x boost should not be a config param, because it is a HW feature

rotate a sd1306 oled?

air101 requires pull-ups?

what to do with documentation of inherited interfaces?

https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html

1 x beschrijving voor module display parameters
maybe gf.horizontal gf.vertical etc. should be global? or east, south, west, north? "E" etc.

class directions
    north =
    north_east =
    east =
    south_east = 
    south =
    south_west = 
    west = 
    north_west = 
    
ESP32 generic spiram on sunton_esp32_2432s028 has no effect at all
on board with soldered spiram?
(not even crash)

build & load arguments separate, any order
target, gf, nogf, spiram, octal, baudrate

time the downloads
pause at end of .bat is useless

more timing data in demos

https://www.openhasp.com/0.7.0/hardware/
[MicroPython image](https://micropython.org/download/GENERIC_S3_SPIRAM_OCT/)

general esp32 discussion, incl. spiram
way to load the nogf images
internal links to the boards
noteer ook interne / externe antennes

luatos c3 - air101 
- cursor - abstraction for such a cursor? asbtract from orientation?
- simple game?


https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/windows

import gc; gc.collect(); print( gc.mem_free() )

- make/load doesn't work
- make/load nogf

- test teensy40, teensy41, rp2040w
- test all downloads
- include godafoss in image name?
- godafoss/g -> godafoss/gf

- help('modules')
- import os; print( os.uname() )

install godafoss as hosted library

board: pycom lopy

inherit:
- no-additions

https://github.com/lemariva/uPyLoRaWAN
- https://github.com/lemariva/uPyLoRaWAN/tree/LoRaWAN

https://snapcraft.io/install/micropython/raspbian
https://gpiozero.readthedocs.io/en/latest/recipes.html
https://sourceforge.net/projects/raspberry-gpio-python/
https://github.com/peterhinch/micropython-touch/

gpio_oc is not implemented!


builds
- now uses latest latest, should use latest stable, or maybe 1.22
- build nogodafoss
- support both for download

https://dev.to/shilleh/how-to-use-esp32-cam-with-micropython-4odo

https://khalsalabs.com/how-to-use-micropython-on-esp32-your-ultimate-free-guide/

https://github.com/micropython/micropython-lib/tree/master/micropython

https://github.com/peterhinch/micropython-nano-gui

https://docs.python.org/3/c-api/memoryview.html

https://github.com/v923z/micropython-ulab?tab=readme-ov-file#stm-based-boards

directly from git, no branch
https://github.com/florisla/stm32loader

https://www.arducam.com/ov2640/

TODO

- Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "godafoss/g/edge.py", line 52, in edge
  File "godafoss/__init__.py", line 166, in __getattr__
  File "<string>", line 1, in <module>
  ImportError: can't import name _edge_esp32  
  doesn't work on .py sources either...
  
- esp8266 build, try with built-in!  
- esp32c3 build
- esp32 build - works!
- pico-w build
- esp32c build
- examples in documentation refer to the old test
- sphinx warnings
- avoid using micropython directly?
- complete introduction build & install
- adc example & test to tests, change import path to root
- add RAM & startup metric to all demos
- suppress base: object

TTGO LORA32 (ESP32-DOWDQ6)
with godafoss 
    intial RAM 163.712 kB
    initial FLASH 2.0 MB
    blink (not edge) time 80 ms, memory 2592 bytes (165344->162752)
without godafoss (bin from site)
    intial RAM 163.408 kB
    initial FLASH 2.0 MB    
idem with /lib/godafoss (.mpy files)
    intial RAM 163312 kB
    initial FLASH 0.872 MB
    blink (not edge) time 14176 ms, memory 4608 bytes (161632->157024)   
idem with /lib/godafoss (.py files)
    intial RAM 163.632 kB
    initial FLASH 0,4 MB
    blink (not edge) time 19330 ms, memory 4784 bytes (161488->156704)
    
- size after import godafoss
- some more-code test for time and memory (edge-kitt, OLED demo)    
    
    

freeze other resources
https://github.com/orgs/micropython/discussions/12094

blink
teensy.py  time 447 ms, memory 8528 bytes (760464->751936)
teensy.mpy time 491 ms, memory 8912 bytes (760464->751552)
rp2040w.py  can't download 
rp2040w.mpy time 3172 ms, memory 12304 bytes (182640->170336)
rp2040.py time 4356 ms, memory 11936 bytes (182864->170928) 1.4M of 1.6M used

kitt
teensy.py  time 796 ms, memory 13968 bytes (760448->746480)
teensy.mpy time 864 ms, memory 14720 bytes (760448->745728)
rp2040w.mpy time 5083 ms, memory 16976 bytes (182624->165648) 812 of 848 kB Flash used
rp2040.py time 6914 ms, memory 16288 bytes (182848->166560)

large LCD
teensy.py  time 1141 ms, memory 181296 bytes (760144->578848)
           time 33452 ms, memory 192784 bytes (760144->567360)
teensy.mpy time 1195 ms, memory 181728 bytes (760112->578384)
           time 34015 ms, memory 193472 bytes (760112->566640)
           
large LCD monochrome 240x320
rp2040.py  time 7843 ms, memory 47792 bytes (182528->134736)


- simple images in a directory, autoloaded p = icon( "python_128_128_bw" )
- make/xxx bijwerken, kan als batch file of als python, from / of from make/
- manier om image te downloaden (getxxx)?
- re-check all LCDs
- lcd-switch demo'ss, must go faster (7735)
- ronde LCD
- generic lcd afmaken
- revisit documentation, quotes from sources, imges
- humidity sensors
- nrf24l01
- lora module + transport abstraction
- re-check the ESP32 edge boards, system name is arbitrary
- nano 33, nano 33 BLE
- dedicated pico board for that parallel LCD and the bigger one
- e-ink displays
- demos: show memory free
- big allocation in lcd: gc first
- tools for nano 33, teensy 4.0, teensy 4.1 build & download (in dockers)
- iets Nx zo groot weergeven
- een paar andere fonts
- dedicated pico board for older 128x64 graphic displays - too many pins....
- LCD overview
- https://github.com/gitcnd/LCDWIKI_SPI/blob/master/LCDWIKI_SPI.cpp
- terminal tool in python

- teensy 4.0 can't store the full library (too many files?)
- version for nano BLE sense, but not for without ble-sense
- esp8266 has no __file__
- __file__ = "godafoss/__init__.py"

- w600 loads OK but no REPL contact??
https://sigmdel.ca/michel/ha/w600/second_look_w600_en.html

- long lines must en in --+ or   |
- lora library
- lorawan library
- port moet een array van pins hebben
- one( "meter" ), zero( value )
- all( ) instead of add?? naddel dat types binnengehaald moeten worden
- hoe documentatie verwerken (intern, extern, voorbeelden)
- shift extend into extend_ne, extenmd_sw etc.; maybe only 'fitting'? Then only N and E...
- print 2 keer zo groot
- verzameling icons
- er is nu 2x defaukt font?
- auto-check file name and rest of header
- rename to pin_in_out_class ??
- tools for generating icons, glyphs, etc
- where did lcd.py go, and how should it be called? lcd_spi_color?
- missing ports from buffer    
- pulse should be a separate function? where should the docstring be?
- documentation, how to handle the forwarding?
- host-run edge board for testing??
- how to check type hints??
- pulse and blink is separate, log too (could also handle port etc.)
- report -> benchmark -> tools
- spi & i2c in godafoss, even if only a thin layer
- why spi but no i2c??
- native pin emulation
- leach more tests and examples from old test/native
- enable/disable overhead via global booleans
- check all files (also the ones that are not host loadable)
- check header comment
- @report("name") timing
- timing report for generic lcd

http://www.lcdwiki.com/1.6inch_SPI_Module_SSD1283A_SKU:MSP1601

https://github.com/orgs/micropython/discussions/13233

WiPy specific stuff on 
    https://docs.micropython.org/en/latest/library/index.html
    
https://github.com/LilyGO/MicroPython-1

https://github.com/peterhinch/micropython-samples/blob/master/README.md#5-module-index

https://github.com/loboris/ESP32_ePaper_example

https://github.com/ZinggJM/GxEPD2

https://github.com/mcauser/micropython-waveshare-epaper

https://github.com/HelTecAutomation/Wireless-Paper

ili9341

line buffer 
240 * 2 = 480 bytes each call
320 calls  
10 MHz 1.51 ms
20 MHz 1.45
makes sense: 240*480*8/20M = 0.06 s
without the write_command calls 1.33 ms
+ avoid the * 1.30 s
+ twice the pixel retrieve 1.7 s
once, no write, avoid *, micropython.native 812 ms
(viper doesn't work, maybe works on the smaller section)
still native, once, explicit loop instead of range 814 ms

python, range, avoid *, write_cmd( buffer = ), line buffer, 20 Mhz
1413 ms
breaks down: 
    pixel retrieve line 400 ms
    write_command 120 ms
    
python, 20 MHz    
for b in self._buffer:
   self.write_command( None, buffer = self._pixels[ b ] )
1.58 ms
self._spi.write( self._pixels[ b ] ) 687 ms  
idem native 680 ms
zonder native, array index out of the loop  670 ms
idem, 2 spi calls 1318 ms -> spi calls now take all time
make the spi calls transfer 2 x the data
   longer _pixels 821 ms (same as -> 10 MHz)
   p + p 995 ms
   
30 MHz 687 ms
20 MHz 691 ms
10 MHz 820 ms

(er wordt iets te veel geschreven - waarom??)

accummulate byte array
1 1214
2 753
4 (64) 690 (varies a lot) 

idem single allocation
1 (16) 970
2 713
4 544
8 464
16 444

This is promising, continue with the 16
base 445
- 2 x spi_write -> 550
- 2 x copy -> 541
- @native -> 398
- separate _send@native 398
- some const 311 !
- viper crashes
- python 355, native 312
- native, copy twice 490
- native, spi twice 417


native, ms, copy to temp
1: 779
2: 529
4: 382
8: 318
16: 311 -> avoid lookup 301
32: 361 (??)
128: 771
    - copy twice 14482
    - spi twice 839
    
explicit copy loop, python
8: 2391  
native 1478

280 ms




