# ===========================================================================
#
# file     : amg8831.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import machine
import godafoss as gf


# ===========================================================================

class amg8831:

    def __init__( 
        self, 
        bus: machine.I2C, 
        address: int = 0,
        init = True
    ) -> None:

        self._bus = bus
        self._address = 0x68 + address
        if init:
            self.init

    # =======================================================================    
    
    def init( self ):
        self.mode_normal()
        gf.sleep_us( 50_000 )
        self.reset_initial()
        gf.sleep_us( 2_000 )
        self.reset_flag()
    
    # =======================================================================    
    
    def register_write( self, register, data ):
        self._bus.writeto_mem( self._address, register, data )

    # =======================================================================    
    
    def register_read( self, register, n ):
        return self._bus.readfrom_mem( self._address, register, n )
  
    # =======================================================================    
    
    def mode_normal( self ):
        return self.register_write( 0x00, byte( 0x00 ) )
  
    # =======================================================================    
    
    def mode_sleep( self ):
        return self.register_write( 0x00, byte( 0x10 ) )
  
    # =======================================================================    
    
    def reset_initial( self ):
        return self.register_write( 0x01, byte( 0x3F ) )
  
    # =======================================================================    
    
    def reset_flag( self ):
        return self.register_write( 0x01, byte( 0x30 ) )
  
    # =======================================================================    
    
    def data( self ):
        return self.register_read( 0x80, 128 )
        
    # =======================================================================    

# ===========================================================================
    