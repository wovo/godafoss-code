# ===========================================================================
#
# file     : sx127x_configuration.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
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
    
    # =======================================================================

    def __init__( 
        self,
        *,
        frequency = 868E6, 
        tx_power = 2, 
        bandwidth = 125E3,    
        spreading_factor = 8, 
        coding_rate = 5, 
        preamble_length = 8,
        implicit_header = False, 
        sync_word = 0x12, 
        enable_crc = False,
        rx_gain = 2,
        rx_boost = True,
        auto_agc = True,
        tx_fifo_base_address = 0,
        rx_fifo_base_address = 0
    ):
        self.frequency = frequency
        self.tx_power = tx_power
        self.bandwidth = bandwidth
        self.spreading_factor = spreading_factor
        self.coding_rate = coding_rate
        self.preamble_length = preamble_length
        self.implicit_header = implicit_header
        self.sync_word = sync_word
        self.enable_crc = enable_crc
        self.rx_gain = rx_gain
        self.rx_boost = rx_boost
        self.auto_agc = auto_agc
        self.tx_fifo_base_address = tx_fifo_base_address
        self.rx_fifo_base_address = rx_fifo_base_address
    
    # =======================================================================
    
# ===========================================================================
    