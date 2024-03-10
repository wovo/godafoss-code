# ===========================================================================
#
# file     : gf__edge.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf
import machine

# ===========================================================================

class _edge:
    
    soft = gf.spi.soft
    hard = gf.spi.hard

    # =======================================================================

    def port( self ):
        return gf.make_port_in_out( self.pins ) 

    # =======================================================================

    def spi( 
        self,
        frequency = 10_000_000,
        polarity = 1,
        phase = 1,
        mechanism: int = 1,        
    ):
        return gf.spi( 
            frequency = frequency,
            polarity = polarity,
            phase = phase,
            sck = self.spi_sck,
            mosi = self.spi_mosi,
            miso = self.spi_miso,
            mechanism = mechanism
        )
    
    # =======================================================================

    def _soft_spi( 
        self,
        baudrate = 10_000_000,
        polarity = 1,
        phase = 1,        
    ):
        return machine.SoftSPI( 
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sck ),
            mosi = machine.Pin( self.spi_mosi ),
            miso = machine.Pin( self.spi_miso )
        )
    
    # =======================================================================

    def _hard_spi(
        self,
        baudrate = 20_000_000,
        polarity = 1,
        phase = 1, 
    ):
        return machine.SPI( 
            baudrate = baudrate,
            polarity = 1,
            phase = 1,
            sck = machine.Pin( self.spi_sck ),
            mosi = machine.Pin( self.spi_mosi ),
            miso = machine.Pin( self.spi_miso )
        )

    # =======================================================================

    def _hard_spi(
        self,
        baudrate = 20_000_000,
        polarity = 1,
        phase = 1, 
    ):
        return gf.spi( 
            baudrate = baudrate,
            polarity = 1,
            phase = 1,
            sck = self.spi_sck,
            mosi = self.spi_mosi,
            miso = self.spi_miso
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
