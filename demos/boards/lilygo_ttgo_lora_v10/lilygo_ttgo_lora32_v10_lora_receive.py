# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_lora32_v10_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
board = gf.board_lilygo_ttgo_lora32_v10()
lora = board.lora()

v = lora.version()
print( f"sx127x version={v}" )

lora.mode_receive_single()
lora.dump_registers()
t0 = gf.time_us()
while True:
    gf.sleep_us( 200_000 )
    if lora.packet_received():
        
        snr = lora.packet_snr()
        rssi = lora.packet_rssi()
        msg = lora.read_payload()
        t = ( gf.time_us() - t0 ) // 1_000_000
        print( f"t={t} snr={snr} rssi={rssi} n={len(msg)}" )
        for i, b in enumerate( msg ):
            print( f"{i}: {b}" )
        
    


