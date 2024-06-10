# ===========================================================================
#
# file     : gf_mcp23017.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class mcp23017( gf._port_in_out_buffer ):

    # =======================================================================    

    def __init__(
        self,
        bus,
        address = 0
    ):
        self._bus = bus
        self._address = 0x20 + address
        self._cmd = bytearray( 2 )        
        gf._port_in_out_buffer.__init__( self, 16 )

    # =======================================================================

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            gf.bytes_from_int( 0x00, 1 )
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x14
        self._bus.write( self._cmd )        
        self._bus.write( gf.bytes_from_int( self._write_buffer, 2 ) )
        self._bus.stop()

    # =======================================================================    

    def directions_flush( self ):
        "write directions buffer to chip"
        self._bus.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x00
        self._bus.write( self._cmd ) 
        self._bus.write( gf.bytes_from_int( self._directions_buffer, 2 ) )
        self._bus.stop()

# ===========================================================================   
