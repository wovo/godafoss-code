# ===========================================================================
#
# file     : chips.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

from godafoss import *

#$$document( 0 )

# ===========================================================================

class ft6236( touch ):
    """
    ft6236 touch screen chip driver
    
    :param i2c: machine.I2C
        i2c bus that connects to the chip, max 10 Mhz       
    
    :param size: :class:`~godafoss.xy`
        the size of the touch area in pixels        
    
    mux settling time 500 clocks???
    rotate and mirror the screen
    offsets & calibration
    general touch class for this??
    """

    # =======================================================================   

    class registers:   
        dev_mode             = const( 0x00 )
        gest_id              = const( 0x01 )
        td_status            = const( 0x02 )
        
        p1_xh                = const( 0x03 )
        p1_xl                = const( 0x04 )
        p1_yh                = const( 0x05 )
        p1_hl                = const( 0x06 )
        p1_weight            = const( 0x07 )
        p1_misc              = const( 0x08 )
        
        p2_xh                = const( 0x09 )
        p2_xl                = const( 0x0A )
        p2_yh                = const( 0x0B )
        p2_hl                = const( 0x0C )
        p2_weight            = const( 0x0D )
        p2_misc              = const( 0x0E )
        
        group                = const( 0x80 )
        th_diff              = const( 0x85 )
        ctrl                 = const( 0x86 )
        time_enter_monitor   = const( 0x87 )
        period_active        = const( 0x88 )
        period_monitor       = const( 0x89 )
        
        radian_value         = const( 0x91 )
        offset_left_right    = const( 0x92 )
        offset_up_down       = const( 0x93 )
        distance_left_right  = const( 0x94 )
        distance_up_down     = const( 0x95 )
        distance_zoom        = const( 0x96 )

        lib_ver_h            = const( 0xA1 )
        lib_ver_l            = const( 0xA2 )
        cipher               = const( 0xA3 )
        g_mode               = const( 0xA4 )
        pwr_mode             = const( 0xA5 )
        firmid               = const( 0xA6 )
        focaltech_id         = const( 0xA6 )
        release_code_id      = const( 0xA6 )
        state                = const( 0xA )

        
    # =======================================================================    

    def __init__(
        self,
        i2c: "machine.I2C",
        size: xy = None,
        address: int = 0x38
    ):
        touch.__init__(
            self,
            size = size,
            span = 4096
        )
        self._i2c = i2c
        self._size = size
        self._address = address
        
    # =======================================================================        

    def touch_adcs( self ):
        
        status, x_high, x_low, y_high, y_low = \
            self._i2c.readfrom_mem( self._address, 2, 5 )
        
        if ( status & 0x03 ) == 0:
            return None, None
        
        else:
            x = ( ( x_high & 0x0F ) << 8 ) + x_low
            y = ( ( y_high & 0x0F ) << 8 ) + y_low
            return x, y
            
    # =======================================================================        

# ===========================================================================


# ===========================================================================

class xpt2046( touch ):
    """
    XPT2046 touch screen chip driver
    
    :param spi: (machine.SPI)
        spi bus that connects to the chip, max 10 Mhz

    :param cs: ($macro_insert make_pin_out_types )
        chip select pin (active low)        
    
    :param size: :class:`~godafoss.xy`
        the size of the touch area in pixels        
    
    mux settling time 500 clocks???
    rotate and mirror the screen
    offsets & calibration
    general touch class for this??
    """

    # =======================================================================   

    class channels:   
        x              = const( 5 )
        y              = const( 1 )
        z1             = const( 3 )
        z2             = const( 4 )
        temperature_0  = const( 0 )
        temperature_1  = const( 7 )
        battery        = const( 2 )
        auxillary      = const( 6 )
        
    # =======================================================================    

    def __init__(
        self,
        spi: "machine.SPI",
        cs: [ int, pin_out, pin_in_out, pin_oc ],
        size: xy = None
    ):
        touch.__init__(
            self,
            size = size,
            span = 4095
        )
        self._spi = spi
        self._cs = make_pin_out( cs )
        self._size = size
        self._rx = bytearray( 3 )
        self._tx = bytearray( 3 )
        
    # =======================================================================        

    def touch_adcs( self ):

        a = self.command_response( channel = self.channels.x )
        b = self.command_response( channel = self.channels.y )
        
        if a == 0 or b == 0:
            return None, None
        
        else:
            return a, b
            
    # =======================================================================
    
    def command_response( 
        self, 
        channel: int = 0, 
        command: int = 0 
    ):
        """
        command / response exchange with the chip
        
        :param channel: int (default 0)
            channel number to read
               
        :param command: int (default 0)
            other command bits; default is single ended, 12 bits
        
        :result: int
            the 12 bit respons from the chip   
            
        This function sends a command to the chip and receives and
        returns the response. 
        The most significan bit (start bit) of the command 
        is automatically set.
        """

        self._tx[ 0 ] = 0x80 | channel << 4 | command
        self._cs.write( 0 )
        self._spi.bus.write_readinto( self._tx, self._rx )
        self._cs.write( 1 )

        return ( self._rx[ 1 ] << 4 ) | ( self._rx[ 2 ] >> 4 )    
    
# ===========================================================================


