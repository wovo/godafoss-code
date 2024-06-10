# ===========================================================================
#
# file     : spi.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class spi:
    """
    $$ref( "https://en.wikipedia.org/wiki/Serial_Peripheral_Interface", "spi" ) 
    bus
    
    :param sck: (int|str)    
        the clock pin
        
    :param mosi: (int|str)    
        the master-out-slave-in pin
        
    :param miso: (int|str)    
        the master-in-slave-out pin
        
    :param frequency: (int)    
        the (maximum) clock frequency
        
    :param mode: (int)    
        the mode (0..3), which determines the polarity and phase; 
        check clock polarity and phase in this
        $$ref( "https://en.wikipedia.org/wiki/Serial_Peripheral_Interface", "spi wiki" )
        
    :param implementation: (int)    
        the
        $$ref( "#spi_implementation" )
        : spi_implementation.soft (default)
        or spi_implementation.hard
        
    :param id: (int)    
        the spi channel id 
        (specifying an id forces the mechansim to 
        be gf.spi_implementation.hard)
        
    All pins must be physical pins of the target (not godafoss pin objects).    
    """
    
    # =======================================================================

    def __init__(
        self,
        sck: int | str,
        mosi: int | str,
        miso: int | str,
        frequency: int = 10_000_000,
        mode: int = 0,
        implementation: int = gf.spi_implementation.soft,
        id: int = None
    ):
    
        self._sck = sck
        self._mosi = mosi
        self._miso = miso
        self._frequency = frequency
        self._mode = mode
        self._implementation = implementation
        
        if self.id is not None:
            self._implementation = gf.spi_implementation.hard
            
        if self._mode == 0:    
            self._polarity, self._phase = 0, 0
            
        elif self._mode == 1:    
            self._polarity, self._phase = 0, 1
            
        elif self._mode == 2:    
            self._polarity, self._phase = 1, 0
            
        elif self._mode == 3:    
            self._polarity, self._phase = 1, 1
            
        else:
            ValueError( "unknown spi mode {self._mode}" )
         
        if self._implementation == gf.spi_implementation.soft:
                
            import machine
            self.bus = machine.SoftSPI( 
                baudrate = self._frequency,
                polarity = self._polarity,
                phase = self._phase,
                sck = self._machine.Pin( self._sck ),
                mosi = self._machine.Pin( self._mosi ),
                miso = self._machine.Pin( self._miso )
            )
                
        elif self._implementation == gf.spi_implementation.hard:
            
            import machine
            if self._id is None:
            
                import os
                uname = os.uname()[ 0 ]
                
                if uname == "rp2":
                    self._id = 0
                    
                elif uname == "mimxrt":
                    self.bus = machine.SPI(
                        1,
                        baudrate = self._frequency,
                        polarity = self._polarity,
                        phase = self._phase
                    )
                    return
                
                else:
                    ValueError( "unknown system (%s), specify the id" % uname )
                
            self._bus = machine.SPI(
                self._id,
                baudrate = self._frequency,
                polarity = self._polarity,
                phase = self._phase,
                sck = machine.Pin( self._self.sck ),
                mosi = machine.Pin( self._self.mosi ),
                miso = machine.Pin( self._self.miso )
            )
                
        else:
            raise ValueError( f"unknown spi implementation {self._implementation}" )

    # =======================================================================

    def write(
        self,
        *args, 
        **kwargs
    ) -> None:
        """
        write parameter(s) to the spi bus
        """

        self._bus.write( 
            *args, 
            **kwargs 
        )
        
    # =======================================================================
        
# ===========================================================================
