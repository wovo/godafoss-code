This is the source repository for 
[godafoss](https://
, a micro-python library.

TODO
====

- now uses latest latest, should use latest stable, or maybe 1.22
- build both with and without godafoss
- support both for download
- esp32 'no module named godafoss'
- canvas_native is not micropython, maybe a few others too

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
- revisit loading, maybe don't search in .mpy mode
- examples in documentation refer to the old test
- sphinx take VERY long
- sphinx warnings
- avoid using micropython directly?
- intro should be at the start of the html file
- don't history on the html file & the images
- complete introduction build & install
- adc example & test to tests, change import path to root
- always look for xxx.mpy in the root, only later search in all subdirs (no need to know suffix)
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
- die dongle ESP32
- e-ink displays
- demos: show memory free
- big allocation in lcd: gc first
- tools for nano 33, teensy 4.0, teensy 4.1 build & download (in dockers)
- iets Nx zo groot weergeven
- een paar andere fonts
- dedicated pico board for older 128x64 graphic displays
- LCD overview
- https://github.com/gitcnd/LCDWIKI_SPI/blob/master/LCDWIKI_SPI.cpp
- terminal tool in python

- teensy 4.0 can't store the full library (too many files?)
- version for nanon BLE sense, but not for without it
- esp8266 has no __file__, limits recursion, and is VERY slow, but blink & kitt work, reset doesn't work
- __file__ = "godafoss/__init__.py"

- w600 loads OK but no REPL contact??

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




