# ===========================================================================
#
# file     : pcf8574x.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
import machine


# ===========================================================================

class _pcf8574x( gf._port_oc_buffer ):
    """
    pcf8574 / pcf8574a I2C I/O extender
    
    This class implements an interface to a pcf8574 or pcf8574a
    I2C I/O extender chip.
    
    $insert_image( "pcf8574-pinout", 1, 300 )
    
    A pcf8574(a) is an I2C slave that provides 8 open-collector 
    input/output pins with weak pull-ups.
    The power supply range is 2.5 .. 5.5 Volt.
    
    The chip has a 7-bit slave address.
    3 bits are set by the level of 3 input pins (a0 .. a2) of the chip.
    The pcf8574 and pcf8574a are the same chips, but with different
    I2C bus addresses.
    With all address poins pulled low the 7-bit i2c address is 
    0x20 (pcf8574) or 0x38 (pcf8574a).
    
    $insert_image( "pcf8574-addresses", 1, 400 )
    
    The chip has only one register, which can be read and written.
    When written, it determines the level of the 8 output pins:
    low when the bit is 0, pulled weakly high when the bit is 1.
    When read, the level of the 8 pins determines the value:
    0 for a low pin, 1 for a high pin.
    To read the input levels, an all-1 value should first be written,
    otherwise the pins that output a 0 (low level) will dominate
    any external circuit attached to thsose pins.
    """

    def __init__( 
        self, 
        bus: machine.I2C, 
        address: int = 0 
    ):
        """
        create a pcf8574x interface
        
        The address must be the 7-bit I2C address.
        """
        self._bus = bus
        self._address = address
        gf._port_oc_buffer.__init__( self, 8 )

    # =======================================================================    

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            gf.bytes_from_int( self._read_buffer, 1 ) 
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.writeto( 
            self._address, 
            gf.bytes_from_int( self._write_buffer, 1 ) 
        )

# ===========================================================================
