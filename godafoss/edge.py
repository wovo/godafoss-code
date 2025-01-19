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
import os
import platform

silent = False

# ===========================================================================

class edge( 
    gf.port_in_out 
):

    """
    generic peripheral test interface

    This class provides the interfaces that my 'edge' test
    boards expect: for each target, a 14-pin header provides
    ground, power (3.3 and 5.0 V), and 8 data pins.
    Some pins have dedicated functions when interfacing to
    typical peripherals:

        pins[ 0 ] : SPI sck
        pins[ 1 ] : SPI mosi
        pins[ 2 ] : SPI miso
        pins[ 3 ] : SPI chip select
        pins[ 4 ] : LCD data / command
        pins[ 5 ] : LCD reset, 1-pin neopixel data
        pins[ 6 ] : LCD backlight, I2C SCL
        pins[ 7 ] : I2C SDA
    
    The actual pins used depend on the target chip,
    as detected by their os.name().
    Target boards with the same chip but different pinouts
    are distinguished by a resistor divider connected to an ADC pin.
    
    The target chip/board detection can be overruled by specifying the
    8 {pins} explicitly.
    
    The class can be used native (CPython on windows or Linux) when 
    a target board is connected that runs the edge().server().
    In that case, a serial {port_name} can be specified (default
    is COM42 on windows). The USB and/or serial communication will
    slow the pin access down significantly.
    """

    # =======================================================================

    def __init__(
        self,
        pins = None,
        port_name = None
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
    
        try:
            s = platform.system()
        except AttributeError:
        
            # MicroPython
            uname = os.uname()
            self._init_pins_from_uname( os.uname() )
            gf.port_in_out.__init__( self, self.pins )
            return
            
        if ( s == "Windows" ) or ( port_name is not None ):
        
            # Windows or Linux native, use a serial proxy
            self.system = f"native on {s} ia proxy on {port_name}"
            self._init_pins_proxy( port_name or "COM42" )
            return
            
        if s != "Linux":
            print( f"native system not recognised '{name}'" ) 
            return
            
        # Linux, no serial port specified
        
        pi = False
        for line in open( "/proc/cpuinfo" ).readlines():
            pi |= line.find( "Raspberry Pi" ) > -1
            
        if pi:
            self.system = "Raspberry Pi native pins"
            self.pins = ( 36, 35, 37, 34, 3, 4, 12, 17 )
            return

        print( "Linux, no Pi, no serial port found" )            

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

    def _init_pins_proxy(
        self,
        serial_port_name: str
    ):
        import serial
        self._serial_port = serial.Serial( 
            serial_port_name, 
            baudrate = 115200,
            timeout = 0.01
        )

        gf.port_in_out.__init__( self )
        self.pins = [
            gf.port_in_out_pin_proxy( self, n )
            for n in range( 8 )
        ]
        self.number_of_pins = len( self.pins )
        self.read = self._proxy_client_read
        self.write = self._proxy_client_write
        self.directions_set = self._proxy_client_directions_set

    # =======================================================================
    
    def _proxy_client_send( 
        self, 
        message 
    ):
        self._serial_port.write( ( message + "\r" ).encode( "utf-8" ) )

    # =======================================================================
    
    def _proxy_client_spin(
        self
    ):
      while True:
        message = self._serial_port.readline().decode( "utf-8" )
        if len( message ) == 0:
            return
            
        if message.startswith( "--r" ):
            try:
                self._result = int( message[ 3: ] )
            except:
                pass
       
        else:
            print( "server:", message, end = "" )
                    
    # =======================================================================

    def _proxy_client_read( self ):
        self._proxy_client_send( "r" )
        self._result = None
        while self._result is None:
            self._proxy_client_spin()
        return self._result

    # =======================================================================

    def _proxy_client_write( self, value ):
        self._proxy_client_spin()
        self._proxy_client_send( f"w{value}" )
        self._proxy_client_spin()

    # =======================================================================

    def _proxy_client_directions_set( self, directions ):
        self._proxy_client_spin()
        self._proxy_client_send( f"d{directions}" )
        self._proxy_client_spin()

    # =======================================================================
    
    def _proxy_server_handle_message(
        self,
        message: str
    ):
        verbose = False
    
        if len( message ) < 1:
            print( f"received empty message" )
            return
            
        c = message[ 0 ]
        try:
            v = int( message[ 1: ] )
        except ( TypeError, ValueError ):
            v = None  
        if verbose:
            print( f"received [{message}] c='{c}' v={v}" )
    
        if c == "d":
            if v is not None:
                if verbose:
                    print( "direction", v )
                self.directions_set( v )

        elif c == "w":
            if v is not None:
                if verbose:
                    print( "write", v )
                self.write( v )

        elif c == "r":
            v = self.read()
            if verbose:
                print( "read", v )
            self._server_print( f"--r{v}" )    
    
    # =======================================================================

    def server(
        self
    ):
        print( "proxy server running" )
        while True:
            self._proxy_server_handle_message( input() )

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

