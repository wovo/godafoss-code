# ===========================================================================
#
# file     : sx127x_configuration.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class sx127x_configuration:

    """
    configuration of an sx127x LoRa Chip
    
    An object of this class holds the configuration parameters used
    to initialize or (re)configure an sx127x chip driver.
    
    """

    def __init__( 
        self,
        *,
        frequency = 868E6, 
        tx_power = 2, 
        signal_bandwidth = 125E3,    
        spreading_factor = 8, 
        coding_rate = 5, 
        preamble_length = 8,
        implicit_header = False, 
        sync_word = 0x12, 
        enable_crc = False,
        rx_gain = 2,
        rx_boost = True,
        auto_agc = True,
    ):
        gf.store_arguments( self, **locals() )
    
    
# ===========================================================================
    