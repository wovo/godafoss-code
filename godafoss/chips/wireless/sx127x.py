# ===========================================================================
#
# file     : sx127x.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


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
        fifo                  = gf.const( 0x00 )
        op_mode               = gf.const( 0x01 )
        frf_msb               = gf.const( 0x06 )
        frf_mid               = gf.const( 0x07 )
        frf_lsb               = gf.const( 0x08 )
        pa_config             = gf.const( 0x09 )
        ocp                   = gf.const( 0x0b )
        lna                   = gf.const( 0x0c )
        fifo_addr_ptr         = gf.const( 0x0d )
        fifo_tx_base_addr     = gf.const( 0x0e )
        fifo_rx_base_addr     = gf.const( 0x0f )
        fifo_rx_current_addr  = gf.const( 0x10 )
        irq_flags             = gf.const( 0x12 )
        rx_nb_bytes           = gf.const( 0x13 )
        pkt_snr_value         = gf.const( 0x19 )
        pkt_rssi_value        = gf.const( 0x1a )
        rssi_value            = gf.const( 0x1b )
        modem_config_1        = gf.const( 0x1d )
        modem_config_2        = gf.const( 0x1e )
        preamble_msb          = gf.const( 0x20 )
        preamble_lsb          = gf.const( 0x21 )
        payload_length        = gf.const( 0x22 )
        modem_config_3        = gf.const( 0x26 )
        freq_error_msb        = gf.const( 0x28 )
        freq_error_mid        = gf.const( 0x29 )
        freq_error_lsb        = gf.const( 0x2a )
        rssi_wideband         = gf.const( 0x2c )
        detection_optimize    = gf.const( 0x31 )
        invertiq              = gf.const( 0x33 )
        detection_threshold   = gf.const( 0x37 )
        sync_word             = gf.const( 0x39 )
        invertiq2             = gf.const( 0x3b )
        dio_mapping_1         = gf.const( 0x40 )
        version               = gf.const( 0x42 )
        pa_dac                = gf.const( 0x4d )    

    # =======================================================================
    
    def __init__(
        self,
        spi: machine.SPI, 
        chip_select: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ],
        configuration: gf.sx127x_configuration = gf.sx127x_configuration()
    ) -> None:
    
        self._spi = spi
        self._chip_select = gf.make_pin_out( chip_select )    

        self.config( configuration )
        
    # =======================================================================
    
    def config( 
        self,
        configuration = None
    ) -> None:
    
        if configuration is None:
            configuration = gf.sx127x_configuration()
    
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
        sf = gf.clamp( sf, 6, 12 );

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
        v |= ( gf.clamp( r, 5, 8 ) - 4 ) << 1
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
        power = gf.clamp( power, 2, 17 ) - 2    
        self.register_write( self.registers.pa_config, 0x80 | power )

    # =======================================================================

    def rx_gain( 
        self,
        gain: int
    ) -> None:
        gain = gf.clamp( gain, 1, 6 )
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
        length = gf.clamp( length, 0, 256 );
        
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




