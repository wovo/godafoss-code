# ===========================================================================
#
# file     : sx127x.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class sx127x:

    """
    sx127x chip driver
    
    This is a driver for the LoRa mode of the Semtech sx127x 
    (sx1272, sx1276, sx1277, sx1278, sx1279 ) series of chips. 
    The FSK/OOK mode of these chips is not supported.
    
    Some of these chips support a smaller range of settings than others.
    It is up to the user to check that the setting is valid
    for the chip that is used. t
    The driver methods just write the setting.
    
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
        data_command: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ],
        chip_select: [ int, gf.pin_out, gf.pin_in_out, gf.pin_oc ],
        configuration: sx127x_configuration = gf.sx127x_configuration()
    ) -> None:
    
        self._spi = spi
        self._data_command = gf.make_pin_out( data_command )
        self._chip_select = gf.make_pin_out( chip_select )    

        self.config( configuration )
        
    # =======================================================================
    
    def config( 
        self,
        configuration: sx127x_configuration 
    ) -> None:
    
        # some settinngs can only be changed in sleep mode
        self.sleep()

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


        self.invert_IQ(self._parameters["invert_IQ"])




        # set base addresses
        self.write_register(REG_FIFO_TX_BASE_ADDR, FifoTxBaseAddr)
        self.write_register(REG_FIFO_RX_BASE_ADDR, FifoRxBaseAddr)
    

    # =======================================================================
    #
    # register access
    #
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

    def register_write(
        self, 
        address: int, 
        value: int
    ) -> None:
        self._chip_select.write( 0 )  
        self._spi.write( bytes( [ address | 0x80, value & 0xFF ] ) )
        self._chip_select.write( 1 )  

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
        f = ( f << 19 ) // 32_000_000
        self.register_write( self.registers.frf_msb, f >> 16 )
        self.register_write( self.registers.frf_mid, f >> 8  )
        self.register_write( self.registers.frf_lsb, f >> 0  )        
    
    # =======================================================================

    def bandwidth( 
        self
        bw: int 
    ) -> None:
        v = 9
        for n, f in enumerate(
            7.8E3, 10.4E3, 15.6E3, 20.8E3, 
            31.25E3, 41.7E3, 62.5E3, 125E3, 250E3
        ):
            if f < bw:
                v = n

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

        if sf == 6:
            self.register_write( self.registers.detection_optimize, 0xc5 )
            self.register_write( self.registers.detection_threshold, 0x0c )
        else:
            self.register_write( self.registers.detection_optimize, 0xc3 )
            self.register_write( self.registers.detection_threshold, 0x0a )
        
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
        v |= ( std::clamp( (int) r, 5, 8 ) - 4 ) << 1
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
        self
        implicit: bool
    ) -> None:
        v = self.register_read( self.registers.modem_config_1 )
        v = v | 0x01 if implicit else v & ~0x01
        self.register_write( self.registers.modem_config_1, v  )        
    
    # =======================================================================

    def sync_word( 
        self,
        w: int 
    ) -> None:
        self.register_write( self.registers.sync_word, w )     

    # =======================================================================

    def crc( 
        self,
        enabled: bool 
    ) -> None:
        v = self.register_read( self.registers.modem_config_2 )
        v = v | 0x04 if enabled else v & ~ 0x04          
        self.register_write( self.registers.modem_config_2, v )       
    
    # =======================================================================

    def tx_power( 
        self, 
        power: int, 
        boost: bool 
    ) -> None:
    
        if boost:
            # 20dBm not supported
            power = std::clamp( power, 2, 17 )
            v = 0x80 | ( power - 2 )
            
        else:
            # probably not correct,  but not used
            p = std::clamp( p, 2, 17 );
            v = 0x40 | ( power - 2 )
            
        self.register_write( self.registers.pa_config, v )

    # =======================================================================

    def rx_gain( 
        self,
        gain: int
    ) -> None:
        gain = std::clamp( gain, 1, 6 )
        v = self.read_register( self.registers.lna )
        v = ( v & 0x1f ) | ( gain << 5 )
        self.write_register( self.registers.lna, v ) 
        
    # =======================================================================

    def rx_boost( 
        self,
        boost: bool 
    ) -> None:
       v = self.read_register( self.registers.lna )
       v = v | 0x03 if boost else v & ~ 0x03 
       self.write_register( self.registers.lna, v )       
    
    # =======================================================================

    def low_data_rate( 
        self,
        ldr: bool 
    ) -> None:
       v = self.read_register( self.registers.modem_config_3 )
       v = v | 0x08 if ldr else v & ~ 0x08 
       self.write_register( self.registers.modem_config_3, v )       
    
    # =======================================================================

    def auto_agc( 
        self,
        auto: bool 
    ) -> None:
       v = self.read_register( self.registers.modem_config_3 )
       v = v | 0x04 if ldr else v & ~ 0x04 
       self.write_register( self.registers.modem_config_3, v )       
    
    # =======================================================================

    // ======================================================================
    //
    // transmit
    //
    // ======================================================================   

    bool transmitting(){
    	auto x = register_read( reg::op_mode );
    	(void) x;
        return ( register_read( reg::op_mode ) & 0x07 ) == 0x03;
    } 

    template< unsigned int s >    
    void transmit( std::array< uint8_t, s > & buffer ){
        _transmit( &buffer[ 0 ], s );
    }    
    
    void _transmit( const uint8_t *buffer, int size ){
        mode_standby();
        size = std::clamp( (int) size, 0, 256 );
        register_write( reg::fifo_tx_base_addr, 0 );
        register_write( reg::fifo_addr_ptr, 0 );
        for( int i = 0; i < size; ++i ){
            register_write( reg::fifo, buffer[ i ] );
        }    
        register_write( reg::payload_length, size );
        mode_transmit();
    }  
    
    // ======================================================================
    //
    // receive
    //
    // ======================================================================
    
    template< unsigned int s >
    void receive( std::array< uint8_t, s > & buffer, int & n ){
        _receive( &buffer[ 0 ], s, n );
    }

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
    
    uint8_t irq_flags(){
        return  register_read( reg::irq_flags );
    }
    
    bool packet_received(){
        
        //register_write( reg::irq_flags, ~ 0x40 );

        auto flags = irq_flags();
        // must be packet-received and not crc error
        if(( flags & 0x60 ) == 0x40 ){
            register_write( reg::irq_flags, 0x60 );
            return true;
        }
        
        // clear a CRC error
        register_write( reg::irq_flags, 0x20 );

        auto mode = register_read( reg::op_mode );
        if(( mode & 0x07 ) < 0x05 ){
            mode_receive_single();    
        }
        
        return false;
    }
    
    
    def packet_rssi( self ) -> int:
        rssi = self.read_register( reg::pkt_rssi_value )
        return (rssi - (164 if self._frequency < 868E6 else 157))

    def packet_snr( self ) -> float:
        snr = self.read_register( reg::pkt_snr_value )
        return snr * 0.25    

        
    
    # =======================================================================

    def begin_packet(self, implicit_header_mode = False):
        self.standby()
        self.implicit_header_mode(implicit_header_mode)

        # reset FIFO address and paload length
        self.write_register(REG_FIFO_ADDR_PTR, FifoTxBaseAddr)
        self.write_register(REG_PAYLOAD_LENGTH, 0)

    def end_packet(self):
        # put in TX mode
        self.write_register(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_TX)

        # wait for TX done, standby automatically on TX_DONE
        while self.read_register(REG_IRQ_FLAGS) & IRQ_TX_DONE_MASK == 0:
            pass

        # clear IRQ's
        self.write_register(REG_IRQ_FLAGS, IRQ_TX_DONE_MASK)

        self.collect_garbage()

    def write(self, buffer):
        currentLength = self.read_register(REG_PAYLOAD_LENGTH)
        size = len(buffer)

        # check size
        size = min(size, (MAX_PKT_LENGTH - FifoTxBaseAddr - currentLength))

        # write data
        for i in range(size):
            self.write_register(REG_FIFO, buffer[i])

        # update length
        self.write_register(REG_PAYLOAD_LENGTH, currentLength + size)
        return size

    def set_lock(self, lock = False):
        self._lock = lock

    def get_irq_flags(self):
        irq_flags = self.read_register(REG_IRQ_FLAGS)
        self.write_register(REG_IRQ_FLAGS, irq_flags)
        return irq_flags



    def standby(self):
        self.write_register(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_STDBY)

    def sleep(self):
        self.write_register(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_SLEEP)

    def set_tx_power(self, level, outputPin = PA_OUTPUT_PA_BOOST_PIN):
        self._tx_power_level = level

        if (outputPin == PA_OUTPUT_RFO_PIN):
            # RFO
            level = min(max(level, 0), 14)
            self.write_register(REG_PA_CONFIG, 0x70 | level)

        else:
            # PA BOOST
            level = min(max(level, 2), 17)
            print( "BOOST PA=%d" % level )
            self.write_register(REG_PA_CONFIG, PA_BOOST | (level - 2))

    def set_frequency(self, frequency):
        self._frequency = frequency

        freq_reg = int(int(int(frequency) << 19) / 32000000) & 0xFFFFFF

        self.write_register(REG_FRF_MSB, (freq_reg & 0xFF0000) >> 16)
        self.write_register(REG_FRF_MID, (freq_reg & 0xFF00) >> 8)
        self.write_register(REG_FRF_LSB, (freq_reg & 0xFF))

    def set_spreading_factor(self, sf):
        sf = min(max(sf, 6), 12)
        self.write_register(REG_DETECTION_OPTIMIZE, 0xc5 if sf == 6 else 0xc3)
        self.write_register(REG_DETECTION_THRESHOLD, 0x0c if sf == 6 else 0x0a)
        self.write_register(
            REG_MODEM_CONFIG_2, 
            (self.read_register(REG_MODEM_CONFIG_2) & 0x0f) | ((sf << 4) & 0xf0)
        )


    def set_coding_rate(self, denominator):
        denominator = min(max(denominator, 5), 8)
        cr = denominator - 4
        self.write_register(
            REG_MODEM_CONFIG_1, 
            (self.read_register(REG_MODEM_CONFIG_1) & 0xf1) | (cr << 1)
        )

    def set_preamble_length(self, length):
        self.write_register(REG_PREAMBLE_MSB,  (length >> 8) & 0xff)
        self.write_register(REG_PREAMBLE_LSB,  (length >> 0) & 0xff)

    def invert_IQ(self, invert_IQ):
        self._parameters["invertIQ"] = invert_IQ
        if invert_IQ:
            self.write_register(
                REG_INVERTIQ,
                (
                    (
                        self.read_register(REG_INVERTIQ)
                        & RFLR_INVERTIQ_TX_MASK
                        & RFLR_INVERTIQ_RX_MASK
                    )
                    | RFLR_INVERTIQ_RX_ON
                    | RFLR_INVERTIQ_TX_ON
                ),
            )
            self.write_register(REG_INVERTIQ2, RFLR_INVERTIQ2_ON)
        else:
            self.write_register(
                REG_INVERTIQ,
                (
                    (
                        self.read_register(REG_INVERTIQ)
                        & RFLR_INVERTIQ_TX_MASK
                        & RFLR_INVERTIQ_RX_MASK
                    )
                    | RFLR_INVERTIQ_RX_OFF
                    | RFLR_INVERTIQ_TX_OFF
                ),
            )
            self.write_register(REG_INVERTIQ2, RFLR_INVERTIQ2_OFF)



    def dump_registers(self):
        for i in range(128):
            print("0x{:02X}: {:02X}".format(i, self.read_register(i)), end="")
            if (i + 1) % 4 == 0:
                print()
            else:
                print(" | ", end="")



    def receive(self, size = 0):
        self.implicit_header_mode(size > 0)
        if size > 0: 
            self.write_register(REG_PAYLOAD_LENGTH, size & 0xff)

        # The last packet always starts at FIFO_RX_CURRENT_ADDR
        # no need to reset FIFO_ADDR_PTR
        self.write_register(
            REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_RX_CONTINUOUS
        )

    def on_receive(self, callback):
        self._on_receive = callback

        if self._pin_rx_done:
            if callback:
                self.write_register(REG_DIO_MAPPING_1, 0x00)
                self._pin_rx_done.irq(
                    trigger=Pin.IRQ_RISING, handler = self.handle_on_receive
                )
            else:
                self._pin_rx_done.detach_irq()

    def handle_on_receive(self, event_source):
        self.set_lock(True)              # lock until TX_Done
        irq_flags = self.get_irq_flags()

        if (irq_flags == IRQ_RX_DONE_MASK):  # RX_DONE only, irq_flags should be 0x40
            # automatically standby when RX_DONE
            if self._on_receive:
                payload = self.read_payload()
                self._on_receive(self, payload)

        elif self.read_register(REG_OP_MODE) != (
            MODE_LONG_RANGE_MODE | MODE_RX_SINGLE
            ):
            # no packet received.
            # reset FIFO address / # enter single RX mode
            self.write_register(REG_FIFO_ADDR_PTR, FifoRxBaseAddr)
            self.write_register(
                REG_OP_MODE, 
                MODE_LONG_RANGE_MODE | MODE_RX_SINGLE
            )

        self.set_lock(False)             # unlock in any case.
        self.collect_garbage()
        return True

    def received_packet(self, size = 0):
        irq_flags = self.get_irq_flags()

        self.implicit_header_mode(size > 0)
        if size > 0: 
            self.write_register(REG_PAYLOAD_LENGTH, size & 0xff)

        # if (irq_flags & IRQ_RX_DONE_MASK) and \
           # (irq_flags & IRQ_RX_TIME_OUT_MASK == 0) and \
           # (irq_flags & IRQ_PAYLOAD_CRC_ERROR_MASK == 0):

        if (irq_flags == IRQ_RX_DONE_MASK):  
            # RX_DONE only, irq_flags should be 0x40
            # automatically standby when RX_DONE
            return True
 
        elif self.read_register(REG_OP_MODE) != (MODE_LONG_RANGE_MODE | MODE_RX_SINGLE):
            # no packet received.
            # reset FIFO address / # enter single RX mode
            self.write_register(REG_FIFO_ADDR_PTR, FifoRxBaseAddr)
            self.write_register(
                REG_OP_MODE, 
                MODE_LONG_RANGE_MODE | MODE_RX_SINGLE
            )

    def read_payload(self):
        # set FIFO address to current RX address
        # fifo_rx_current_addr = self.read_register(REG_FIFO_RX_CURRENT_ADDR)
        self.write_register(
            REG_FIFO_ADDR_PTR, 
            self.read_register(REG_FIFO_RX_CURRENT_ADDR)
        )

        # read packet length
        if self._implicit_header_mode:
            packet_length = self.read_register(REG_PAYLOAD_LENGTH)  
        else:
            packet_length = self.read_register(REG_RX_NB_BYTES)

        payload = bytearray()
        for i in range(packet_length):
            payload.append(self.read_register(REG_FIFO))

        self.collect_garbage()
        return bytes(payload)







