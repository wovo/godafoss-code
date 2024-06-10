# ===========================================================================
#
# file     : gf__edge.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
#import machine

# ===========================================================================

class _edge:

    # =======================================================================

    def port_in_out( self ):
        return gf.make_port_in_out( self.pins ) 

    # =======================================================================

    def port_in( self ):
        return gf.make_port_in( self.pins ) 

    # =======================================================================

    def port_out( self ):
        return gf.make_port_out( self.pins ) 

    # =======================================================================

    def spi( 
        self,
        frequency = 10_000_000,
        mode: int = 0,
        mechanism: int = 1,   
        implementation: int = gf.spi_implementation.soft,
        id: int = None        
    ):
        return gf.spi( 
            sck = self.spi_sck,
            mosi = self.spi_mosi,
            miso = self.spi_miso,
            frequency = frequency,
            mode = mode,
            implementation = implementation,
            id = id
        )

    # =======================================================================

    def soft_i2c(
        self,
        frequency = 100_000
    ):
        return machine.SoftI2C(
            freq = frequency,
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        ) 
    
    # =======================================================================

    def hard_i2c(
        self,
        frequency = 100_000
    ):        
        return machine.SoftI2C(
            freq = frequency,            
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        )                            

    # =======================================================================
    
# ===========================================================================
