# ===========================================================================
#
# file     : gf_hd44780_pcf8574.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def hd44780_pcf8574( 
    size: gf.xy, 
    bus, 
    address = 7
) -> gf.hd44780:
    chip = gf.pcf8574( bus, address )
    data = gf.make_port_in_out( chip.p4, chip.p5, chip.p6, chip.p7 ) # chip.selection()
    rs = chip.p0
    e = chip.p2
    rw = chip.p1
    backlight = chip.p3
    return gf.hd44780( size, data, rs, e, rw, backlight )    
     
     
# =========================================================================== 
