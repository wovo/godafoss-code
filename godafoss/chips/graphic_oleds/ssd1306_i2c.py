# ===========================================================================
#
# file     : gf_ssd1306_i2c.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
import machine

class ssd1306_i2c( gf.ssd1306_base ):
    """
    ssd1306 i2c monochrome oled display driver
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param i2c: (machine.I2C)
        i2c bus that connects to the chip
    
    :param background: (bool)
        background 'color', default (False) is off
    
    :param address: (int)
        7-bit i2c slave address, default is 0x3C

    This is an i2c driver for the i2c ssd1306 monochrome oled controller.
    This chip is used in various cheap oled displays and modules.
    
    #$insert_image( "ssd1306-i2c", 1, 200 )
    
    $macro_insert canvas_monochrome    
    """

    # =======================================================================

    def __init__( 
        self, 
        size: xy, 
        i2c: machine.I2C, 
        background = False, 
        address = 0x3C
    ) -> None:
        self._i2c = i2c
        self._address = address
        self._cmd = bytearray( 2 )
        gf.ssd1306_base.__init__(
            self,
            size = size,
            background = background
        )

    # =======================================================================

    def write_command( 
        self, 
        cmd: int 
    ) -> None:
        """
        write a command byte to the chip
        
        :param command: (int)
            the command byte to be send to the chip
        
        This method writes a single command byte to the chip.
        """
        
        self._cmd[ 0 ] = 0x80  # Co=1, D/C#=0
        self._cmd[ 1 ] = cmd
        self._i2c.writeto( self._address, self._cmd )

    # =======================================================================

    def _write_framebuf( self ) -> None:
        self._i2c.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x40 # set_disp_start_line?
        self._i2c.write( self._cmd )
        self._i2c.write( self._buffer )
        self._i2c.stop()
        
    # =======================================================================
        
#============================================================================
