# ===========================================================================
#
# file     : gf_edge.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024, 2025
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
silent = False

# ===========================================================================

class edge( gf.port_in_out ):
    """
    generic peripheral test interface

    This class provides the interfaces that my 'edge' test
    target boards provide: for each target, a 14-pin header provides
    ground, power (3.3 and 5.0 V), and 8 data pins (p0..p7).
    Some pins have dedicated functions when interfacing to
    typical peripherals:

    v-div
    native
    pins


    """

    # =======================================================================

    def __init__(
        self,
        pins = None,
        port_name = "COM42"
    ) -> None:

        if pins is not None:
            gf.pin_in_out.__init__( self, pins )
        else:
            self._init_pins( port_name )

        if not silent:
            print( f"edge board is {self.system}" )
            print( f"edge pins are {self.pins}" )

        # (soft) SPI
        self.spi_sck = self.pins[ 0 ]
        self.spi_mosi = self.pins[ 1 ]
        self.spi_miso = self.pins[ 2 ]

        # lcd
        self.chip_select = self.pins[ 3 ]
        self.data_command = self.pins[ 4 ]
        self.reset = self.pins[ 5 ]
        self.backlight = self.pins[ 6 ]

        # (soft) I2C
        self.i2c_scl = self.pins[ 6 ]
        self.i2c_sda = self.pins[ 7 ]

        # neopixels
        self.neopixel_data = self.pins[ 5 ]

    # =======================================================================

    def _init_pins(
        self,
        port_name: str
    ) -> None:

        import os
        try:
            uname = os.uname()
        except AttributeError:
            uname = None
            
        if uname is not None:
            self._init_pins_from_uname( os.uname() )
            gf.port_in_out.__init__( self, self.pins )

        else:
            import platform
            name = platform.system()
            self._init_pins_native( name, port_name )

    # =======================================================================

    def _init_pins_from_uname(
        self,
        uname
    ) -> None:

        if uname[ 0 ] == "rp2":
            result = gf._edge_rp2()

        elif uname[ 0 ] == "esp32":

            if uname[ 4 ] == "ESP32C3 module with ESP32C3":
                result = gf._edge_esp32c3()

            elif uname[ 4 ] == "LOLIN_S2_PICO with ESP32-S2FN4R2":
                self.system = "Lolin S2 PICO"
                self.pins = ( 36, 35, 37, 34, 3, 4, 12, 17 )

            elif uname[ 4 ] == "LOLIN_C3_MINI with ESP32-C3FH4":
                result = gf._edge_esp32_lolin_c3_mini()

            else:
                result = gf._edge_esp32()

        elif uname[ 0 ] == "esp8266":
            self.system = "ESP8266"
            self.pins = ( 14, 13, 12, 15, 0, 2, 5, 4 )

        elif uname[ 0 ] == "mimxrt":
            self.system = "Teensy 4.1"
            self.pins = ( 27, 26, 1, 17, 18, 19, 20, 21 )

        else:
            print( "unknow uname:", uname[ 0 ] )

    # =======================================================================

    def _edge_rp2(
        self
    ) -> None:

        v = gf.gpio_adc( 28 ).read().scaled( 0, 65535 )

        # 10k, 10k
        if gf.within( v, 31000, 35000 ):

            self.system = "original RP2040 rp2 or rp2w"
            self.pins = ( 18, 19, 16, 17, 26, 27, 13 , 12 )


        # 10k, 15k
        elif gf.within( v, 24000, 28000 ):

            self.system = "01Space RP2040-0.42 OLED"
            self.pins = ( 20, 24, 25, 26, 5, 6, 4, 3 )

        else:
            print( f"rp2 unrecognized adc( 28 ) = {v}" )

    # =======================================================================

    def _init_pins_native(
        self,
        name: str,
        port_name: str
    ) -> None:

        if name == "Windows":
            self.system = f"native on windows via proxy on {port_name}"
            self._init_pins_proxy( port_name )

        else:
            print( f"native system not recognised '{name}'" )

    # =======================================================================

    # proxy-to-server server commands
    _direction_low = gf.const( 0x10 )
    _direction_high = gf.const( 0x20 )
    _write_low = gf.const( 0x30 )
    _write_high = gf.const( 0x40 )
    _read_low = gf.const( 0x50 )
    _read_high = gf.const( 0x60 )

    # =======================================================================

    def _init_pins_proxy(
        self,
        serial_port_name: str
    ):
        import serial
        self._serial_port = serial.Serial( serial_port_name )

        gf.port_in_out.__init__( self )
        self.pins = [
            gf.port_in_out_pin_proxy( self, n )
            for n in range( 8 )
        ]
        self.number_of_pins = len( self.pins )
        self.read = self._read
        self.write = self._write
        self.directions_set = self._directions_set

    # =======================================================================
    
    def _send( 
        self, 
        byte 
    ):
        print( "send %02X" % byte )
        self._serial_port.write( byte )

    # =======================================================================

    def _read( self ):
        self._send( self._read_low )
        self._send( self._read_high )
        byte = ser.read()
        result = byte & 0x0F
        byte = ser.read()
        result = result | ( ( byte & 0x0F ) << 4 )
        return result

    # =======================================================================

    def _write( self, value ):
        self._send( self._write_low | ( value & 0x0F ) )
        self._send( self._write_high | ( ( value >> 4 ) & 0x0F ) )

    # =======================================================================

    def _directions_set( self, directions ):
        self._send( self._direction_low | ( directions & 0x0F ) )
        self._send( self._direction_high | ( ( directions >> 4 ) & 0x0F ) )

    # =======================================================================
    
    def _server_handle_byte(
        self,
        byte
    ):
    
        if ( byte & 0xF0 ) == self._direction_low:
            for i in range( 4 ):
                self.pins[ i ].direction_set( byte & 0x01 )
                byte = byte >> 1

        elif ( byte & 0xF0 ) == self._direction_high:
            for i in range( 4, 8 ):
                self.pins[ i ].direction_set( byte & 0x01 )
                byte = byte >> 1

        elif ( byte & 0xF0 ) == self._write_low:
            for i in range( 4 ):
                v = byte & 0x01
                self.pins[ i ].write( byte & 0x01 )
                byte = byte >> 1

        elif ( byte & 0xF0 ) == self._write_high:
            for i in range( 4, 8 ):
                self.pins[ i ].write( byte & 0x01 )
                byte = byte >> 1

        elif ( byte & 0xF0 ) == self._read_low:
            byte  = 0
            for i in range( 7, 3, -1 ):
                byte = byte << 1
                byte |= self.pins[ i ].read()
            print( self._read_high | byte, end = '' )

        elif ( byte & 0xF0 ) == self._read_high:
            byte  = 0
            for i in range( 7, 3, -1 ):
                byte = byte << 1
                byte |= self.pins[ i ].read()
            print( self._read_high | byte, end = '' )    
    
    # =======================================================================

    def server(
        self
    ):
        import sys
        while True:
            self._server_handle_byte( sys.stdin.read( 1 ) )

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

