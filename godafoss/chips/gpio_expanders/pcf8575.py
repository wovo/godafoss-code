# ===========================================================================
#
# file     : gf_pcf8575.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

#$$document( 0 )


# ===========================================================================

class pcf8575( gf._port_oc_buffer ):
    """
    pcf8575 I2C I/O extender
    
    This class implements an interface to a pcf8575
    I2C I/O extender chip.
    
    $$insert_image( "pcf8575-pinout", 300 )
    
    A pcf8575 is an I2C slave that provides 8 open-collector 
    input/output pins with weak pull-ups.
    The power supply range is 2.5 .. 5.5 Volt.
    
    $$insert_image( "pcf8575-iopin", 300 )
    
    The chip has a 7-bit slave address.
    3 bits are set by the level of 3 input pins (a0 .. a2) of the chip.
    With all address poins pulled low the i2c address is 0x20.
    
    $$insert_image( "pcf8575-addresses", 300 )
    
    The chip has only one register, which can be read and written.
    When written, it determines the level of the 8 output pins:
    low when the bit is 0, pulled weakly high when the bit is 1.
    When read, the level of the 8 pins determines the value:
    0 for a low pin, 1 for a high pin.
    
    $$insert_image( "pcf8575-diagram", 300 )
    
    The next code shows a kitt display
    on 8 LEDs connected to the pcf8574 output pins.
    Because the output pins are open-collector, the LEDs
    are connected to power (instead of to the ground), hence
    the use of hwlib::port_out_invert().
    
    $-$document( 0 )
    .. literalinclude:: examples/pcf8574-kitt.py
       :language: python
       :linenos:
    $-$document( 1 )   
    """

    # =======================================================================    

    def __init__( self, bus, address = 0x20 ):
        self._bus = bus
        self._address = address
        gf._port_oc_buffer.__init__( self, 16 )

    # =======================================================================    

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            gf.bytes_from_int( self._read_buffer, 2 ) 
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.writeto( 
            self._address, 
            gf.bytes_from_int( self._write_buffer, 2 ) 
        )

# ===========================================================================   
