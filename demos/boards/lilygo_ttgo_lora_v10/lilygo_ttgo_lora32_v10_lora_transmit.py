# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_lora32_lora_transmit.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_lora32_v10()
lora = board.lora()
display = board.display()

v = lora.version()
print( f"sx127x version={v}" )

n = 0
while True:
    n += 1
    display.clear()
    display.write( gf.text( f"transmit {n}" ) )
    display.flush()
    lora.transmit( bytes( f"hello {n}", "utf-8" ) )
    gf.sleep_us( 1_000_000 )
        
    


