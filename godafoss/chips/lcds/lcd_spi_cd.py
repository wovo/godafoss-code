# ===========================================================================
#
# file     : lcd_spi_cd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import machine
import godafoss as gf


# ===========================================================================

class lcd_spi_cd:
    """
    lcd interface for spi and command/data
    
    :param spi: ($$ref( "gf.spi" ) )
        spi interface (miso not used)
        
    :param data_command: ( int | str | $$ref( "can_pin_out" ) )
        data / command pin, high for data, low for command
        
    :param chip_select: ( int | str | $$ref( "can_pin_out" ) )
        chip select pin, active low
    
    This class provides the basic command & data interface
    for a spi LCD with a command / data pin.
    """

    # =======================================================================    

    def __init__(
        self,
        spi: "gf.spi", 
        data_command: int | str | gf.can_pin_out,
        chip_select: int | str | gf.can_pin_out,
    ) -> None:
        self._spi = spi
        self._data_command = gf.pin_out( data_command )
        self._chip_select = gf.pin_out( chip_select )

    # =======================================================================    

    def write_command(
        self, 
        command: [ int, [ int ] ] = None, 
        data = None,
        buffer = None
    ) -> None:
        """
        write command and/or data
        
        :param command: (None, int)
            a command byte to be send to the lcd
        
        :param data: (None, sequence of bytes)
            data bytes to be send to the lcd
        
        This method writes a command (integer, optional)
        and data (also optional) to the lcd.
        The data must be acceptabel for a bytes() call.
        """
        
        self._chip_select.write( 0 )

        if command is not None: 
            self._data_command.write( 0 )
            #print( command )
            if isinstance( command, int ):
                command = [ command ]
            #print( comand )    
            self._spi.write( bytearray( command ) )
            #self._chip_select.write( 1 )
        
        if data is not None:
            self._data_command.write( 1 )
            #self._chip_select.write( 0 )
            self._spi.write( bytes( data ) )
            
        if buffer is not None:
            self._data_command.write( 1 )
            #self._chip_select.write( 0 )
            self._spi.write( buffer )
            
        self._chip_select.write( 1 )    

    # =======================================================================    

# ===========================================================================    
