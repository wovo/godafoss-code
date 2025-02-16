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

class sx127x_configuration:

    """
    configuration of an sx127x LoRa Chip
    
    An object of this class holds the configuration parameters used
    to initialize or (re)configure an sx127x chip driver.
    
    """
    
    # =======================================================================

    def __init__( 
        self,
        *,
        frequency = 868E6, 
        tx_power = 2, 
        bandwidth = 125E3,    
        spreading_factor = 8, 
        coding_rate = 5, 
        preamble_length = 8,
        implicit_header = False, 
        sync_word = 0x12, 
        enable_crc = False,
        rx_gain = 2,
        rx_boost = True,
        auto_agc = True,
        tx_fifo_base_address = 0,
        rx_fifo_base_address = 0
    ):
        self.frequency = frequency
        self.tx_power = tx_power
        self.bandwidth = bandwidth
        self.spreading_factor = spreading_factor
        self.coding_rate = coding_rate
        self.preamble_length = preamble_length
        self.implicit_header = implicit_header
        self.sync_word = sync_word
        self.enable_crc = enable_crc
        self.rx_gain = rx_gain
        self.rx_boost = rx_boost
        self.auto_agc = auto_agc
        self.tx_fifo_base_address = tx_fifo_base_address
        self.rx_fifo_base_address = rx_fifo_base_address
    
    # =======================================================================
    

# ===========================================================================

class sx127x:

    """
    sx127x chip driver
    
    This is a driver for the LoRa mode of the Semtech sx127x 
    (sx1272, sx1276, sx1277, sx1278, sx1279) series of chips. 
    The FSK/OOK mode of these chips is not supported.
    The driver supports the boost_tx pin, not the 'normal' tx pin.
    
    Some of these chips support a smaller range of settings than others.
    It is up to the user to check that each setting is valid
    for the chip that is used.
    The driver methods write each setting without checking for a
    specific chip.
    
    The driver supports raw LoRa, not LoRaWAN.
    """

    class registers:
        fifo                  = const( 0x00 )
        op_mode               = const( 0x01 )
        frf_msb               = const( 0x06 )
        frf_mid               = const( 0x07 )
        frf_lsb               = const( 0x08 )
        pa_config             = const( 0x09 )
        ocp                   = const( 0x0b )
        lna                   = const( 0x0c )
        fifo_addr_ptr         = const( 0x0d )
        fifo_tx_base_addr     = const( 0x0e )
        fifo_rx_base_addr     = const( 0x0f )
        fifo_rx_current_addr  = const( 0x10 )
        irq_flags             = const( 0x12 )
        rx_nb_bytes           = const( 0x13 )
        pkt_snr_value         = const( 0x19 )
        pkt_rssi_value        = const( 0x1a )
        rssi_value            = const( 0x1b )
        modem_config_1        = const( 0x1d )
        modem_config_2        = const( 0x1e )
        preamble_msb          = const( 0x20 )
        preamble_lsb          = const( 0x21 )
        payload_length        = const( 0x22 )
        modem_config_3        = const( 0x26 )
        freq_error_msb        = const( 0x28 )
        freq_error_mid        = const( 0x29 )
        freq_error_lsb        = const( 0x2a )
        rssi_wideband         = const( 0x2c )
        detection_optimize    = const( 0x31 )
        invertiq              = const( 0x33 )
        detection_threshold   = const( 0x37 )
        sync_word             = const( 0x39 )
        invertiq2             = const( 0x3b )
        dio_mapping_1         = const( 0x40 )
        version               = const( 0x42 )
        pa_dac                = const( 0x4d )    

    # =======================================================================
    
    def __init__(
        self,
        spi: "machine.SPI", 
        chip_select: [ int, can_pin_out ],
        configuration: sx127x_configuration = sx127x_configuration()
    ) -> None:
    
        self._spi = spi
        self._chip_select = make_pin_out( chip_select )    

        self.config( configuration )
        
    # =======================================================================
    
    def config( 
        self,
        configuration = None
    ) -> None:
    
        if configuration is None:
            configuration = sx127x_configuration()
    
        # some settings can only be changed in sleep mode
        self.mode_sleep()

        self.frequency( configuration.frequency )
        self.bandwidth( configuration.bandwidth  )
        self.spreading_factor( configuration.spreading_factor )
        self.coding_rate( configuration.coding_rate )
        self.preamble_length( configuration.preamble_length )        
        self.sync_word( configuration.sync_word )  
        self.enable_crc( configuration.enable_crc )  
        self.header( implicit = configuration.implicit_header )  
        self.tx_power( configuration.tx_power )  
        self.rx_gain( configuration.rx_gain )
        self.rx_boost( configuration.rx_boost )
        self.auto_agc( configuration.auto_agc )
        self.low_data_rate( 
            1000 / ( 
                configuration.bandwidth / 
                2 ** configuration.spreading_factor 
            ) > 16 
        )
        self.tx_fifo_base_address = configuration.tx_fifo_base_address
        self.rx_fifo_base_address = configuration.rx_fifo_base_address        
    
    # =======================================================================
    #
    # register access
    #
    # =======================================================================

    def register_write(
        self, 
        address: int, 
        value: int
    ) -> None:
        self._chip_select.write( 0 )  
        self._spi.write( bytes( [ address | 0x80, value & 0xFF ] ) )
        self._chip_select.write( 1 )  
        
    # =======================================================================
    
    def register_read(
        self, 
        address: int
    ) -> int:
        self._chip_select.write( 0 )  
        self._spi.write( bytes( [ address ] ) )
        response = bytearray( 1 )
        self._spi.readinto( response )
        self._chip_select.write( 1 )  
        return int( response[ 0 ] )

    # =======================================================================
    
    def version( self ) -> int:
        return self.register_read( self.registers.version )
        
    # =======================================================================
    
    def irq_flags( self ) -> int:
        flags = self.register_read( self.registers.irq_flags )  
        #self.register_write( self.registers.irq_flags, flags )          
        return flags
    
    def dump_registers( self ):
        for name, address in (
            ( "fifo",                  self.registers.fifo ),
            ( "op_mode",               self.registers.op_mode ),
            ( "frf_msb",               self.registers.frf_msb ),
            ( "frf_mid",               self.registers.frf_mid ),
            ( "frf_lsb",               self.registers.frf_lsb ),
            ( "pa_config",             self.registers.pa_config ),
            ( "ocp",                   self.registers.ocp ),
            ( "lna",                   self.registers.lna ),
            ( "fifo_addr_ptr",         self.registers.fifo_addr_ptr ),
            ( "fifo_tx_base_addr ",    self.registers.fifo_tx_base_addr ),
            ( "fifo_rx_base_addr",     self.registers.fifo_rx_base_addr ),
            ( "fifo_rx_current_addr",  self.registers.fifo_rx_current_addr ),
            ( "irq_flags",             self.registers.irq_flags ),
            ( "rx_nb_bytes",           self.registers.rx_nb_bytes ),
            ( "pkt_snr_value",         self.registers.pkt_snr_value ),
            ( "pkt_rssi_value",        self.registers.pkt_rssi_value ),
            ( "rssi_value",            self.registers.rssi_value ),
            ( "modem_config_1",        self.registers.modem_config_1 ),
            ( "modem_config_2",        self.registers.modem_config_2 ),
            ( "preamble_msb",          self.registers.preamble_msb ),
            ( "preamble_lsb",          self.registers.preamble_lsb ),
            ( "payload_length",        self.registers.payload_length ),
            ( "modem_config_3",        self.registers.modem_config_3 ),
            ( "freq_error_msb",        self.registers.freq_error_msb ),
            ( "freq_error_mid",        self.registers.freq_error_mid ),
            ( "freq_error_lsb",        self.registers.freq_error_lsb ),
            ( "rssi_wideband",         self.registers.rssi_wideband ),
            ( "detection_optimize",    self.registers.detection_optimize ),
            ( "invertiq",              self.registers.invertiq ),
            ( "detection_threshold",   self.registers.detection_threshold ),
            ( "sync_word",             self.registers.sync_word ),
            ( "invertiq2",             self.registers.invertiq2 ),           
            ( "dio_mapping_1",         self.registers.dio_mapping_1 ),
            ( "version",               self.registers.version ),        
            ( "pa_dac",                self.registers.pa_dac ),        
        ):
            v = self.register_read( address )
            print( f"{address:02X} {name:22} {v:02X}" )

    # =======================================================================
    #
    # All mode_* functions also keep the radio mode LoRa
    #
    # =======================================================================
    
    def mode_sleep( self ):
    
        # must write twice: once to get into sleep,
        # once to change the radio mode to LoRa, 
        # because aparently the mode can only be changed when
        # *in* sleep, not even when *entering* sleep
        
        self.register_write( self.registers.op_mode, 0x80 )
        self.register_write( self.registers.op_mode, 0x80 )
    
    # =======================================================================

    def mode_standby( self ):
        self.register_write( self.registers.op_mode, 0x81 )
    
    # =======================================================================

    def mode_transmit( self ):
        self.register_write( self.registers.op_mode, 0x83 )
    
    # =======================================================================

    def mode_receive_continuous( self ):
        self.register_write( self.registers.op_mode, 0x85 ) 
    
    # =======================================================================

    def mode_receive_single( self ):
        self.register_write( self.registers.op_mode, 0x86 )    

    # =======================================================================
    #
    # radio settings
    #
    # =======================================================================
    
    def frequency( 
        self, 
        f: int 
    ) -> None:
        f = int( f )
        self._frequency = f
        f = ( f  << 19 ) // 32_000_000
        self.register_write( self.registers.frf_msb, f >> 16 )
        self.register_write( self.registers.frf_mid, f >> 8  )
        self.register_write( self.registers.frf_lsb, f >> 0  )     
    
    # =======================================================================

    def bandwidth( 
        self,
        bw: int 
    ) -> None:
        v = 9
        for n, f in enumerate( (
            7.8E3, 10.4E3, 15.6E3, 20.8E3, 
            31.25E3, 41.7E3, 62.5E3, 125E3, 250E3
        ) ):
            if f <= bw:
                v = n
                
        print( "bw v=", v )

        old = self.register_read( self.registers.modem_config_1 )
        self.register_write( 
             self.registers.modem_config_1, ( old & 0x0f ) | ( v << 4 ) 
        )
        
    # =======================================================================

    def spreading_factor( 
        self,
        sf: int 
    ) -> None:
        sf = clamp( sf, 6, 12 );

        self.register_write( 
            self.registers.detection_optimize, 
            0xc5 if sf == 6 else 0xc3 
        )
        self.register_write( 
            self.registers.detection_threshold, 
            0x0c if sf == 6 else 0x0a 
        )
        
        old = self.register_read( self.registers.modem_config_2 )
        self.register_write( 
            self.registers.modem_config_2, 
            ( old & 0x0f ) | ( sf << 4 )  
        )          
    
    # =======================================================================

    def coding_rate( 
        self,
        r: int 
    ) -> None:
        v = self.register_read( self.registers.modem_config_1 )
        v &= 0xf1
        v |= ( clamp( r, 5, 8 ) - 4 ) << 1
        self.register_write( self.registers.modem_config_1, v )         
    
    # =======================================================================

    def preamble_length( 
        self,
        length: int 
    ) -> None:
        self.register_write( self.registers.preamble_msb, length >> 8 )
        self.register_write( self.registers.preamble_lsb, length >> 0 )   

    # =======================================================================

    def header( 
        self,
        implicit: bool
    ) -> None:
        v = self.register_read( self.registers.modem_config_1 )
        v = ( v | 0x01 ) if implicit else ( v & ~0x01 )
        self.register_write( self.registers.modem_config_1, v  )        
    
    # =======================================================================

    def sync_word( 
        self,
        w: int 
    ) -> None:
        self.register_write( self.registers.sync_word, w )     

    # =======================================================================

    def enable_crc( 
        self,
        enabled: bool 
    ) -> None:
        v = self.register_read( self.registers.modem_config_2 )
        v = ( v | 0x04 ) if enabled else ( v & ~ 0x04 )          
        self.register_write( self.registers.modem_config_2, v )       
    
    # =======================================================================

    def tx_power( 
        self, 
        power: int
    ) -> None:
        # only boost pin supporeted
        power = clamp( power, 2, 17 ) - 2    
        self.register_write( self.registers.pa_config, 0x80 | power )

    # =======================================================================

    def rx_gain( 
        self,
        gain: int
    ) -> None:
        gain = clamp( gain, 1, 6 )
        v = self.register_read( self.registers.lna )
        v = ( v & 0x1f ) | ( gain << 5 )
        self.register_write( self.registers.lna, v ) 
        
    # =======================================================================

    def rx_boost( 
        self,
        boost: bool 
    ) -> None:
       v = self.register_read( self.registers.lna )
       v = ( v | 0x03 ) if boost else ( v & ~ 0x03 )
       self.register_write( self.registers.lna, v )       
    
    # =======================================================================

    def low_data_rate( 
        self,
        ldr: bool 
    ) -> None:
       v = self.register_read( self.registers.modem_config_3 )
       v = ( v | 0x08 ) if ldr else ( v & ~ 0x08 )
       self.register_write( self.registers.modem_config_3, v )       
    
    # =======================================================================

    def auto_agc( 
        self,
        auto: bool 
    ) -> None:
       v = self.register_read( self.registers.modem_config_3 )
       v = ( v | 0x04 ) if auto else ( v & ~ 0x04 )
       self.register_write( self.registers.modem_config_3, v )       
    
    # =======================================================================
    #
    # transmit
    #
    # =======================================================================

    def transmitting( self ) -> bool:
        return \
            ( self.register_read( self.registers.op_mode ) & 0x07 ) == 0x03
    
    # =======================================================================

    def transmit(
        self,
        buffer,
        length: int = None,
        wait: bool = True
    ) -> None:
    
        self.mode_standby()
        
        if length is None:
            length = len( buffer )
        length = clamp( length, 0, 256 );
        
        self.register_write( 
            self.registers.fifo_tx_base_addr, 
            self.tx_fifo_base_address 
        )
        self.register_write( 
            self.registers.fifo_addr_ptr, 
            self.tx_fifo_base_address 
        )
        
        for i in range( length ):
            self.register_write( self.registers.fifo, buffer[ i ] )
        self.register_write( self.registers.payload_length, length )
        
        _ = self.irq_flags()
        self.mode_transmit()
        while wait and self.transmitting():
            pass
    
    # =======================================================================
    #
    # receive
    #
    # =======================================================================
    
    def packet_rssi( self ) -> int:
        rssi = self.register_read( self.registers.pkt_rssi_value )
        return (rssi - (164 if self._frequency < 868E6 else 157))

    # =======================================================================

    def packet_snr( self ) -> float:
        snr = self.register_read( self.registers.pkt_snr_value )
        return snr * 0.25 
    
    # =======================================================================
    
    def read_payload( self ) -> bytearray:
    
        # set FIFO address to current RX address
        self.register_write(
            self.registers.fifo_addr_ptr, 
            self.register_read( self.registers.fifo_rx_current_addr )
        )

        packet_length = self.register_read( self.registers.rx_nb_bytes )

        payload = bytearray()
        for i in range( packet_length ):
            payload.append( self.register_read( self.registers.fifo ) )

        return bytes( payload )    
    
    # =======================================================================

    """
        self.register_write( 
            self.registers.fifo_rx_base_addr, 
            configuration.rx_fifo_base_address 
        )    
    
    void _receive( uint8_t *buffer, int size, int & n ){
        
        register_write( reg::fifo_rx_current_addr, 0 );    
        mode_receive_single();

        //dump();

        while( ! packet_received() ){}
        //dump();

        n = std::clamp( (int) register_read( reg::rx_nb_bytes ), 0, size );
        register_write( 
            reg::fifo_addr_ptr, 
            register_read( reg::fifo_rx_current_addr ) 
        );
        for( int i = 0; i < n; ++i ){
            buffer[ i ] = register_read( reg::fifo );
        }
    }
    """
    
    def packet_received( self ) -> bool:
        
        #self.register_write( self.registers.irq_flags, ~ 0x40 )
        
        flags = self.register_read( self.registers.irq_flags )
        
        # must be packet-received and not crc error
        if ( flags & 0x60 ) == 0x40:
            self.register_write( self.registers.irq_flags, 0x60 )
            return True
        
        # clear a CRC error
        self.register_write( self.registers.irq_flags, 0x20 )

        mode = self.register_read( self.registers.op_mode );
        if ( mode & 0x07 ) < 0x05:
            self.mode_receive_single()   
        
        return False;

    def receive(self, size = 0):
        
        self.implicit_header_mode(size > 0)
        if size > 0: 
            self.register_write(REG_PAYLOAD_LENGTH, size & 0xff)

        # The last packet always starts at FIFO_RX_CURRENT_ADDR
        # no need to reset FIFO_ADDR_PTR
        self.register_write(
            REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_RX_CONTINUOUS
        )



# ===========================================================================

class ds1302: 

    def __init__( 
        self, 
        bus, 
        reset = 0,
        address = 0x29
    ):    
        self.bus = bus
        self.address = address
        self.leds = leds
        self.bus.writeto( self.address, b'\x80\x03' )
        self.bus.writeto( self.address, b'\x81\x2B' )

    def read( self ):
        self.bus.writeto( self.address, b'\xB4' )
        data = self.bus.readfrom( self.address, 8 )
        clear = data[ 0 ] + ( data[ 1 ] << 8 )
        red = data[ 2 ] + ( data[ 3 ] << 8 )
        green = data[ 4 ] + ( data[ 5 ] << 8 )
        blue = data[ 6 ] + ( data[ 7 ] << 8 )
        m = max( red, green, blue )
        print( clear, red, green, blue )
        return color( red, green, blue )      
        
    def demo( self ):
        print( "tcs3472 color sensor demo" )
        while True:
            # print( self.read() )
            self.read()
            time.sleep_us( 500_000 )

# ===========================================================================

class amg8831:

    def __init__( 
        self, 
        bus: "machine.I2C", 
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
        sleep_us( 50_000 )
        self.reset_initial()
        sleep_us( 2_000 )
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
    


# ===========================================================================

class _pcf8574x( 
    port_oc_proxy
):
    """
    pcf8574 / pcf8574a I2C I/O extender
    
    This class implements an interface to a pcf8574 or pcf8574a
    I2C I/O extender chip.
    
    $insert_image( "pcf8574-pinout", 1, 300 )
    
    A pcf8574(a) is an I2C slave that provides 8 open-collector 
    input/output pins with weak pull-ups.
    The power supply range is 2.5 .. 5.5 Volt.
    
    The chip has a 7-bit slave address.
    3 bits are set by the level of 3 input pins (a0 .. a2) of the chip.
    The pcf8574 and pcf8574a are the same chips, but with different
    I2C bus addresses.
    With all address poins pulled low the 7-bit i2c address is 
    0x20 (pcf8574) or 0x38 (pcf8574a).
    
    $insert_image( "pcf8574-addresses", 1, 400 )
    
    The chip has only one register, which can be read and written.
    When written, it determines the level of the 8 output pins:
    low when the bit is 0, pulled weakly high when the bit is 1.
    When read, the level of the 8 pins determines the value:
    0 for a low pin, 1 for a high pin.
    To read the input levels, an all-1 value should first be written,
    otherwise the pins that output a 0 (low level) will dominate
    any external circuit attached to thsose pins.
    """

    def __init__( 
        self, 
        bus, #: machine.I2C, 
        address: int = 0 
    ):
        """
        create a pcf8574x interface
        
        The address must be the 7-bit I2C address.
        """
        self._bus = bus
        self._address = address
        port_oc_proxy.__init__( self, 8 )

    # =======================================================================    

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            bytes_from_int( self._read_buffer, 1 ) 
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.writeto( 
            self._address, 
            bytes_from_int( self._write_buffer, 1 ) 
        )


# ===========================================================================

class pcf8574( 
    _pcf8574x 
):
    
    def __init__(
        self,
        bus,
        address = 0
    ):
        """
        create a pcf8574 interface
        
        The address is the 3 bits formed by A0 .. A2.
        """    
        pcf8574x.__init__( self, bus, 0x20 + address )


# ===========================================================================

class pcf8574a( 
    _pcf8574x 
):

    def __init__(
        self,
        bus,
        address = 0
    ):
        """
        create a pcf8574 interface
        
        The address is the 3 bits formed by A0 .. A2.
        """    
        pcf8574x.__init__( self, bus, 0x38 + address )



# ===========================================================================

class pcf8575( 
    port_oc_proxy
):
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
        port_oc_proxy.__init__( self, 16 )

    # =======================================================================    

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            bytes_from_int( self._read_buffer, 2 ) 
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.writeto( 
            self._address, 
            bytes_from_int( self._write_buffer, 2 ) 
        )

# ===========================================================================   

# ===========================================================================

class servo:
    """
    drive a hobby servo

    $insert_image( "servo-sg90", 1, 400 )

    This class drives a hobby servo.
    A hobby servo requires pulses with a width of 1.0 ... 2.0 ms
    (exact range might vary by servo) each 20 ms (this interval is
    not very critical).

    $insert_image( "servo-pulse", 1, 300 )

    These pulse will cause the servo to turn its axle and horn to
    a specific angle.
    Typically, the angle varies between 0 and 180 degrees for pulses
    of 1.0 .. 2.0 ms.

    $insert_image( "servo-angles", 1, 400 )

    Provided that it is called often enough (either write() or poll())
    a servo object will provide a pulse of the appropriate width on the pin.
    The pulse will be delivered by the write() or poll() function call,
    so that call can take up to the maximum pulse length.

    A hobby servo needs a 5V supply, from which it can draw a significant
    current.
    One small (SG90, as shown in the picture) servo can safely
    be powered from a USB port.
    For more and/or larger servos, a separate 5V power suply is advisable.

    $insert_image( "servo-connector", 1, 400 )

    A hobby servo expects a 5V pulse, but in practice a 3.3V GPIO
    pin works fine. If the micro-controller seems to work unreliable
    when driving a servo, adding a large decoupling capacitor on the
    5V power supply (1000uF) can help.
    """

    def __init__(
        self,
        pin: [ int, can_pin_out ],
        minimum: int = 1_000,
        maximum: int = 2_000,
        interval: int = 20_000
    ):
        self._pin = pin_out( pin )
        self._minimum = minimum
        self._maximum = maximum
        self._interval = interval
        self._next = 0
        self._value = None

    def poll( self ) -> None:
        """
        output servo pulse when it is time to do so

        Write a pulse to the servo (corresponding to the last
        fraction written) if it is time to do so.
        The default (bit banged) implementation requires
        poll() to be called regularly.
        An implementation that uses hardware probbaly doesn't need
        poll() calls.
        """

        t = time_us()
        if ( self._value is not None ) and ( t >= self._next ):
            self._pin.pulse(
                self._value.scaled( self._minimum, self._maximum ),
                0
            )
            self._next = t + self._interval

    def write( 
        self, 
        value: fraction 
    ) -> None:
        """
        set servo setpoint

        Write the fraction to the servo as setpoint,
        which causes the corresponding servo pulse to be output the servo
        whenever it is time to do so.

        The default implementation requires write() or poll()
        to be called regularly to create the servo pulses.
        """

        self._value = value
        self.poll()

    def demo( self, steps = 100, iterations = None ) -> None:
        """servo demo"""

        print( "servo demo" )
        for dummy in repeater( iterations ):
            for v in range( 0, steps ):
                self.write( fraction( v, steps ) )
                self.poll()
                sleep_us( self._interval + 1_000 )
            for v in range( steps, 0, -1 ):
                self.write( fraction( v, steps ) )
                self.poll()
                sleep_us( self._interval + 1_000 )


# ===========================================================================

class mcp23017( 
    port_in_out_proxy 
):

    # =======================================================================    

    def __init__(
        self,
        bus,
        address = 0
    ):
        self._bus = bus
        self._address = 0x20 + address
        self._cmd = bytearray( 2 )        
        port_in_out_proxy.__init__( self, 16 )

    # =======================================================================

    def refresh( self ):
        "read buffer from chip"
        self._bus.writeto( 
            self._address, 
            bytes_from_int( 0x00, 1 )
        )

    # =======================================================================    

    def flush( self ):
        "write buffer to chip"
        self._bus.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x14
        self._bus.write( self._cmd )        
        self._bus.write( bytes_from_int( self._write_buffer, 2 ) )
        self._bus.stop()

    # =======================================================================    

    def directions_flush( self ):
        "write directions buffer to chip"
        self._bus.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x00
        self._bus.write( self._cmd ) 
        self._bus.write( bytes_from_int( self._directions_buffer, 2 ) )
        self._bus.stop()

# ===========================================================================   

class mrfc522:
    "Hello"

    class status:
        OK = 0
        NOTAGERR = 1
        ERR = 2

    class cmd:
        REQIDL = 0x26
        REQALL = 0x52
        AUTHENT1A = 0x60
        AUTHENT1B = 0x61

    def __init__( 
        self, 
        spi, 
        cs: [ int, can_pin_out ], 
        rst: [ int, can_pin_out ], 
    ):
        "hello"
        self._spi = spi
        self._cs = make_pin_out( cs )
        self._rst = make_pin_out( rst )
        self.reset()
        
    def reset( self ):        
        self._rst.write( 0 )
        self._cs.write( 1 )
        self._rst.write( 1 )

        self.register_write( 0x01, 0x0F )
        
        self.register_write( 0x2A, 0x8D )
        self.register_write( 0x2B, 0x3E )
        self.register_write( 0x2D,   30 )
        self.register_write( 0x2C,    0 )
        self.register_write( 0x15, 0x40 )
        self.register_write( 0x11, 0x3D )
        self.antenna_on()

    def register_write( self, reg, val ):
        "hello"
        self._cs.write( 0 )
        self._spi.write( b'%c' % int(0xff & ((reg << 1) & 0x7e)) )
        self._spi.write( b'%c' % int(0xff & val) )
        self._cs.write( 1 )

    def register_read( self, reg ):
        "hello"
        self._cs.write( 0 )
        self._spi.write(b'%c' % int(0xff & (((reg << 1) & 0x7e) | 0x80)))
        val = self._spi.read( 1 )
        self._cs.write( 1 )
        return val[ 0 ]

    def _sflags(self, reg, mask):
        "hello"
        self.register_write( reg, self.register_read( reg ) | mask )

    def _cflags(self, reg, mask):
        "hello"
        self.register_write( reg, self.register_read( reg ) & (~mask) )

    def _tocard( self, cmd, send ):
        "hello"
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = self.status.ERR

        if cmd == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30

        self.register_write( 0x02, irq_en | 0x80 )
        self._cflags( 0x04, 0x80 )
        self._sflags( 0x0A, 0x80 )
        self.register_write( 0x01, 0x00 )

        for c in send:
            self.register_write( 0x09, c )
        self.register_write( 0x01, cmd )

        if cmd == 0x0C:
            self._sflags( 0x0D, 0x80 )

        i = 2000
        while True:
            n = self.register_read( 0x04 )
            i -= 1
            if ~(( i != 0 ) and ~( n & 0x01 ) and ~( n & wait_irq )):
                break

        self._cflags( 0x0D, 0x80 )

        if i:
            if ( self.register_read( 0x06) & 0x1B ) == 0x00:
                stat = self.status.OK

                if n & irq_en & 0x01:
                    stat = self.status.NOTAGERR
                elif cmd == 0x0C:
                    n = self.register_read( 0x0A )
                    lbits = self.register_read( 0x0C ) & 0x07
                    if lbits != 0:
                        bits = ( n - 1 ) * 8 + lbits
                    else:
                        bits = n * 8

                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16

                    for _ in range( n ):
                        recv.append( self.register_read( 0x09 ) )
            else:
                stat = self.status.ERR

        return stat, recv, bits

    def _crc( self, data ):
        "hello"
        self._cflags( 0x05, 0x04 )
        self._sflags( 0x0A, 0x80 )

        for c in data:
            self.register_write( 0x09, c )

        self.register_write( 0x01, 0x03 )

        i = 0xFF
        while True:
            n = self.register_read( 0x05 )
            i -= 1
            if not (( i != 0 ) and not ( n & 0x04 )):
                break

        return [self.register_read( 0x22 ), self.register_read( 0x21 ) ]

    def antenna_on( self, on = True ):
        "hello"
        if on and ~( self.register_read(0x14) & 0x03 ):
            self._sflags( 0x14, 0x03 )
        else:
            self._cflags( 0x14, 0x03 )

    def request( self, mode ):
        "hello"
        self.register_write( 0x0D, 0x07 )
        ( stat, recv, bits ) = self._tocard( 0x0C, [ mode ] )

        if ( stat != self.status.OK ) | ( bits != 0x10 ):
            stat = self.status.ERR

        return stat, bits

    def anticoll( self ):
        "hello"
        ser_chk = 0
        ser = [ 0x93, 0x20 ]

        self.register_write( 0x0D, 0x00 )
        ( stat, recv, bits ) = self._tocard( 0x0C, ser )

        if stat == self.status.OK:
            if len( recv ) == 5:
                for i in range( 4 ):
                    ser_chk = ser_chk ^ recv[ i ]
                if ser_chk != recv[ 4 ]:
                    stat = self.status.ERR
            else:
                stat = self.status.ERR

        return stat, recv

    def select_tag( self, ser ):
        "hello"
        buf = [ 0x93, 0x70 ] + ser[ : 5 ]
        buf += self._crc( buf )
        ( stat, recv, bits ) = self._tocard( 0x0C, buf )
        if ( stat == self.status.OK ) and ( bits == 0x18 ):
            return self.status.OK
        else:
            return self.status.ERR

    def auth( self, mode, addr, sect, ser ):
        "hello"
        return self._tocard(0x0E, [ mode, addr ] + sect + ser[ : 4 ] )[ 0 ]

    def stop_crypto1( self ):
        "hello"
        self._cflags( 0x08, 0x08 )

    def read( self, addr ):
        "hello"
        data = [ 0x30, addr ]
        data += self._crc( data )
        ( stat, recv, _ ) = self._tocard( 0x0C, data )
        return recv if stat == self.status.OK else None

    def write( self, addr, data ):
        "hello"
        buf = [ 0xA0, addr ]
        buf += self._crc( buf )
        ( stat, recv, bits ) = self._tocard( 0x0C, buf )

        if ( stat != self.status.OK ) or (bits != 4) or ((recv[0] & 0x0F) != 0x0A):
            stat = self.status.ERR
        else:
            buf = []
            for i in range( 16 ):
                buf.append( data[ i ] )
            buf += self._crc( buf )
            ( stat, recv, bits ) = self._tocard( 0x0C, buf )
            if ( stat != self.status.OK ) or (bits != 4) or ((recv[0] & 0x0F) != 0x0A):
                stat = self.status.ERR

        return stat
        
    def read_uid( self ):
        ( stat, tag_type ) = self.request( self.cmd.REQIDL )
        if stat != self.status.OK:
            return None
            
        ( stat, raw_uid ) = self.anticoll()
        if stat != self.status.OK:
            return None
            
        return ( raw_uid[ 0 ] << 24 ) + ( raw_uid[ 1 ] << 16 ) + ( raw_uid[ 2 ] << 8 ) + raw_uid[ 3 ]  

    def demo( self ):
        "hello"
        print( "mrfc522 card reader demo" )
        n = 0
        while True:

            ( stat, tag_type ) = self.request( self.cmd.REQIDL )

            if stat == self.status.OK:

                ( stat, raw_uid ) = self.anticoll()

                if stat == self.status.OK:
                    n += 1
                    print( "%d New card detected" % n )
                    print( "  - tag type: 0x%02x" % tag_type)
                    print( "  - uid     : 0x%02x%02x%02x%02x" %
                        (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print()

                    if self.select_tag( raw_uid ) == self.status.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if ( self.auth(self.cmd.AUTHENT1A, 8, key, raw_uid)
                            == self.status.OK 
                        ):
                            print( "Address 8 data: %s" % self.read( 8 ) )
                            self.stop_crypto1()
                        else:
                            print( "Authentication error" )
                    else:
                        print( "Failed to select tag" )

# ===========================================================================

class slf3s_1300f:
    """
    sensirion slf3s_1300f flow sensor
    
    can nack (ENODEV) when polled to fast (500us pause)
   
    """
    
    # =======================================================================    

    class commands:   
        """chip commands"""
    
        # common
        start_measuring_water         = const( 0x3608 )
        start_measuring_isopropyl     = const( 0x3615 )
        stop_measuring                = const( 0x3FF9 )
        read_id_and_serial_1          = const( 0x367C )
        read_id_and_serial_2          = const( 0xE102 )
        measure_thermal_conductivity  = const( 0x3646 )
        
    # =======================================================================    

    def __init__( 
        self, 
        i2c: "machine.I2C",
        address: int = 8
    ) -> None:
        self.i2c = i2c
        self.address = address
        self.fluid = self.commands.start_measuring_water
        
        # general call reset and reset time
        # this seems to be required
        self.i2c.writeto( 0x00, bytes( [ 0x06 ] ) )
        sleep_us( 25_000 )
        
        self._reading = False
        
    # =======================================================================    

    def write_command( 
        self, 
        command: int
    ) -> None:
        """
        write a 16-bit command
        """
        
        self.i2c.writeto(
            self.address,
            bytes( ( ( command >> 8 ) & 0xFF, command & 0xFF ) )
        )
        
    # =======================================================================    

    def read_data( 
        self,
        n: int 
    ):
        return self.i2c.readfrom( self.address, n )
    
    # =======================================================================    

    def start_reading(
        self,
        fluid: int = None
    ):
        if fluid is not None:
            self.fluid = fluid
        self.write_command( self.fluid )
        sleep_us( 15_000 )
        self._reading = True
        
    # =======================================================================    

    def stop_reading( self ):
        self.write_command( self.commands.stop_measuring )
        sleep_us( 500 )
        self.reading = False
        
    # =======================================================================
    
    def get_product_id_and_serial_number( self ):
        if self._reading:
            self.stop_reading()
        self.write_command( self.commands.read_id_and_serial_1 )
        self.write_command( self.commands.read_id_and_serial_2 )
        return self.read_data( 18 )    
    
    # =======================================================================
    
    def get_flow_data(
        self,
        n_bytes: int
    ):
        if not self._reading:
            self.start_reading()
        return self.read_data( n_bytes )    

    # =======================================================================    

    def get_flow( self ):
        d = self.get_flow_data( 3 )
        return int_from_bytes(
            ( d[ 1 ], d[ 0 ] ),
            signed = True
        )
    
    # =======================================================================    

    def get_temperature( self ):
        d = self.get_flow_data( 6 )
        return temperature(
            int_from_bytes(
                ( d[ 4 ], d[ 3 ] ),
                signed = True
            ) / 200.0,
            temperature.scale.celcius
        )
    
    # =======================================================================    

    def get_flags( self ):
        d = self.get_flow_data( 9 )
        return int_from_bytes( ( d[ 8 ], d[ 7 ] ) )
    
    # =======================================================================
    
    def get_product_id( self ):
        d = self.get_product_id_and_serial_number()
        return int_from_bytes( ( 
            d[ 4 ], d[ 3 ], 
            d[ 1 ], d[ 0 ] 
        ) )
    
    # =======================================================================
    
    def get_serial_number( self ):
        d = self.get_product_id_and_serial_number()
        return int_from_bytes( ( 
            d[ 16 ], d[ 15 ], 
            d[ 13 ], d[ 12 ],
            d[ 10 ], d[ 9 ], 
            d[ 7 ], d[ 6 ]             
        ) )
    
    # =======================================================================
    
    def demo(
        self,
        fluid: int = None
    ):
        print( "Sensirion SLF3S_1300F demo" )
        print( "product id 0x%08X" % self.get_product_id() )
        print( "serial number %d" % self.get_serial_number() )
        
        cumulative = 0
        n = 0
        last = ticks_us()
        while True:
            n += 1
            now = ticks_us()
            flow = self.get_flow()
            cumulative += flow * ( now - last ) / 1_000_000.0
            last = now
            sleep_us( 1_000 )
            temp = self.get_temperature()
            print( "[%04d] flow %5d;  cumulative %f ml;  temp %s" %
                ( n, flow, cumulative / ( 500.0 * 60.0 ), temp ) )
            sleep_us( 1_000_000 )


# ===========================================================================

class sr04:
    """
    SR04 ultrasonic distance sensor

    $insert_image( "sr04-module", 1, 300 )

    This classs interfaces to an sr04 ultrasonic distance sensor.

    An sr04 measures distance by outputting a short burst
    of utrasonic sound, and listening for an echo caused
    by the reflection of the sound by an object.
    An sr04 requires 5V power.

    $insert_image( "sr04-timing", 1, 400 )

    A measuremment cycle starts with the micro-controller
    putting a short (10us) pulse on the trigger pin.
    This causes the sr04 to output the ultrasonic sound burst
    and listen to the echo.
    The sr04 outputs a pulse that starts with the sound burst,
    and ends with the receiving of the echo.
    The duration of this pulse is proportional to the distance.
    """

    def __init__(
        self,
        trigger: [ int, pin_out, pin_in_out, pin_oc ],
        echo: [ int, pin_in, pin_in_out, pin_oc ],
        speed_of_sound: int = 343,
        minimum_waiting: int = 100_000,
        timeout: int = 100_000
    ):
        """
        sr04 driver constructor

        An sr04 requires a trigger pin (output) and an echo pin (input).
        The trigger input theoretically requires a 5V pulse,
        but in practice a 3.3V works fine.
        The echo output is a 5V pulse.
        Most micro-controller input pins are not 5V compatible,
        so a level shift is needed.
        In practice a simple 1k / 2k2 resistor voltage divider
        works fine.

        To calculate the distance form the echo,
        the speed of sound in air is required.
        The default is 343 m/s, which is
        the value for 20 degrees and standard atmospheric pressure.
        This is probably OK for all practical use.

        After a measurement a minumum waiting interval is required,
        otherwise the previous echo could be picked up.
        The default minimum waiting interval is 100 ms.

        When no pulse is received from the sr04 within the timeout
        a measurement is assumed to have failed.
        The default timeput is 100 ms.
        """

        self._trigger = make_pin_out( trigger )
        self._echo = make_pin_in( echo )
        self.speed_of_sound = speed_of_sound
        self.minimum_waiting = minimum_waiting
        self.timeout = timeout
        self._timeout = 0
        self._result = None
        self._trigger.write( 0 )

    def read(
            self,
            default: int | None = None
        ) -> int | None:

        """
        the distance im mm as integer

        This function measures and returns the distance in mm,
        or the default (by default, None) specied by the caller
        if no valid measurement could be made.

        If less than mimimum waiting interval has expired since
        the previous measurement, no new measurement is taken
        and the previous result is returned.

        When the start or end of the measurement pulse is not seen within
        the timeout, the default value (by default: None) is returned.

        The measurement and waiting for the pulse (or the timeout)
        is done in the function, so a function call can take up to
        the timout time to return.

        Outputting the pulse and listening for the echo is
        done in the function call, so a call can take up to the
        timeout time to return.
        """

        if self._timeout > ticks_us():
            # print( 'too quick' )
            return self._result

        # don't attempt to measure again within the minimum interval
        self._timeout = ticks_us() + self.minimum_waiting

        # echo should be zero before trigger
        if self._echo.read():
            print( 'not zero' )
            return default

        # send 10us trigger
        self._trigger.pulse( 10, 0 )

        # wait for start of measurement pulse
        t1 = ticks_us()
        while not self._echo.read():
            t2 = ticks_us()
            if ( t2 - t1 ) > self.timeout:
                print( 'no start' )
                return default

        # wait for end of measurement pulse
        t1 = ticks_us()
        # print( "echo", self._echo.read() )
        while self._echo.read():
            t2 = ticks_us()
            if ( t2 - t1 ) > self.timeout:
                print( 'no end' )
                return default
        t2 = ticks_us()

        # print( "pulse=", t1, t2, t2 - t1 )
        self._result = (( t2 - t1 ) * self.speed_of_sound ) // ( 2 * 1_000 )
        # print( "res=", self._result )
        return self._result

    def demo( 
        self, 
        interval: int = 500_000, 
        iterations = None 
    ):
        """sr04 demo"""
        print( "sr04 ultrasonic distance sensor demo" )
        for _ in repeater( iterations ):
            # print( 'measure' )
            print( "%d mm" % self.read( default = 9999 ) )
            sleep_us( interval )


# ===========================================================================

class tcs3472:

    def __init__( self, bus, address = 0x29, leds = None ):
        self.bus = bus
        self.address = address
        self.leds = leds
        self.bus.writeto( self.address, b'\x80\x03' )
        self.bus.writeto( self.address, b'\x81\x2B' )

    def read( self ):
        self.bus.writeto( self.address, b'\xB4' )
        data = self.bus.readfrom( self.address, 8 )
        clear = data[ 0 ] + ( data[ 1 ] << 8 )
        red = data[ 2 ] + ( data[ 3 ] << 8 )
        green = data[ 4 ] + ( data[ 5 ] << 8 )
        blue = data[ 6 ] + ( data[ 7 ] << 8 )
        m = max( red, green, blue )
        print( clear, red, green, blue )
        return color( red, green, blue )      
        
    def demo( self ):
        print( "tcs3472 color sensor demo" )
        while True:
            # print( self.read() )
            self.read()
            time.sleep_us( 500_000 )
            
