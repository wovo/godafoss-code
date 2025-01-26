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


# ===========================================================================

class edge( 
    gf.port_in_out 
):

    """
    generic peripheral test interface

    This class provides the interfaces that my 'edge' test
    boards expect: for each target, a 14-pin header provides
    ground, power (3.3 and 5.0 V), and 8 data pins.
    The class implements the interfaec of an 8-pin port_in_out.
    
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
    When run on a Raspberry Pi by defaulkt the GPIO pins are used ditrectly.
    This requires the=at RPi.GPIO is installed and that the application
    can access the GPIO pins (using sudo will do).
    
    The target chip/board detection can be overruled by specifying the
    8 {pins} explicitly.
    
    The class can be used native (CPython on Windows or Linux) when 
    a target board is connected that runs the edge().server().
    In that case, a serial {port_name} can be specified (default
    is COM42 on windows).
    When running on a Raspberry Pi a {port_name} must be specified,
    because by default the GPIO of the Pi are used.
    
    The USB and/or serial communication will
    slow the pin access down significantly.
    """

    # =======================================================================

    def __init__(
        self,
        pins = None,
        port_name: str = None
    ) -> None:

        if pins is None:
            self._init_pins( port_name )
        else:
            gf.pin_in_out.__init__( self, pins )

        print( f"edge board is {self.system}" )

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
            self._init_pins_from_uname()
            gf.port_in_out.__init__( self, self.pins )
            return
            
        print( s )    
        if ( s == "Windows" ) or ( port_name is not None ):
        
            # Windows or Linux native, use a serial proxy
            if port_name is None:
                port_name = "COM42"
            self.system = f"native on {s} via proxy on {port_name}"
            self._init_pins_proxy( port_name )
            return
            
        if s != "Linux":
            print( f"native system not recognised '{name}'" ) 
            return
            
        # running on Linux, no serial port specified
        
        raspberry_pi = False
        for line in open( "/proc/cpuinfo" ).readlines():
            raspberry_pi |= line.find( "Raspberry Pi" ) > -1
            
        if raspberry_pi:
            self.system = "Raspberry Pi native pins"
            self.pins = ( 11, 10, 9, 8, 4, 18, 3, 2 )
            gf.port_in_out.__init__( self, self.pins )
            return

        print( "Linux, not Pi, and no serial port found" )            

    # =======================================================================

    def _init_pins_from_uname(
        self
    ) -> None:
    
        uname = os.uname()

        if uname[ 0 ] == "rp2":
            result = self._edge_rp2()

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

        v = gf.pin_adc( 28 ).read().scaled( 0, 65535 )

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
    ) -> None:
    
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
        self._ignore = ""
        self._proxy_client_check_server()

    # =======================================================================
    
    def _proxy_client_check_server( 
        self
    ) -> None:
    
        import time
        self._result = None
        self._proxy_client_send( "i" )
        for i in range( 10 ):
            time.sleep( 0.01 )
            self._proxy_client_spin()
            if self._result is not None:
                print( self._result.rstrip() )
                if not self._result.startswith( "godafoss edge server" ):
                    print( "unexpected response" )
                return
        print( "no proxy server found" )

    # =======================================================================
    
    def _proxy_client_send( 
        self, 
        message: str 
    ) -> None:
    
        self._ignore = message
        self._serial_port.write( ( message + "\r" ).encode( "utf-8" ) )

    # =======================================================================
    
    def _proxy_client_spin(
        self
    ) -> None:
    
        # don't overflow our transmit buffer
        #import time
        #time.sleep( 0.001 )
    
        while True:
            message = self._serial_port.readline().decode( "utf-8" )
            if len( message ) == 0:
                return
                
            elif message.startswith( "--i" ):
                self._result = message[ 3: ]            
            
            elif message.startswith( "--r" ):
                try:
                    self._result = int( message[ 3: ] )
                except:
                    pass
       
            # This seems to work, but would fail when the echo
            # of a message is received after the next message
            # is sent.
            elif message.rstrip() == self._ignore:
                self._ignore = ""
            
            else:
                print( "server:", message, end = "" )
                    
    # =======================================================================

    def _proxy_client_read( 
        self 
    ) -> None:
    
        self._proxy_client_send( "r" )
        self._result = None
        while self._result is None:
            self._proxy_client_spin()
        return self._result

    # =======================================================================

    def _proxy_client_write( 
        self, 
        value: int
    ) -> None:
    
        self._proxy_client_send( f"w{value}" )
        self._proxy_client_spin()

    # =======================================================================

    def _proxy_client_directions_set( 
        self, 
        directions: int 
    ) -> None:
    
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
            print( f"--r{v}" )    
    
        elif c == "i":
            print( f"--igodafoss edge server on {self.system}" )    
    
    # =======================================================================

    def server(
        self
    ) -> None:
    
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

