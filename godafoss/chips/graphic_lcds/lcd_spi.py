# ===========================================================================
#
# file     : lcd_spi.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the lcd_spi class.
#
# ===========================================================================

import machine
import godafoss as gf


# ===========================================================================

class lcd_spi:
    """
    spi lcd command / data
    
    :param spi: (machine.SPI)
        spi interface (miso not used)
        
    :param data_command: ($macro_insert make_pin_out_types)
        data / command pin, high for data, low for command
        
    :param chip_select: ($macro_insert make_pin_out_types)
        chip select pin, active low
    
    This class provides the basic command & data interface
    for a spi LCD with a command / data pin.
    """

    # =======================================================================    

    def __init__(
        self,
        spi: machine.SPI, 
        data_command: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ],
        chip_select: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ]
    ) -> None:
        self._spi = spi
        self._data_command = gf.make_pin_out( data_command )
        self._chip_select = gf.make_pin_out( chip_select )

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
