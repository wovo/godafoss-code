# ===========================================================================
#
# file     : neopixels.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf

#$$document( 0 )


# ===========================================================================

class neopixels( gf.canvas ):
    """
    neopixels common driver

    :param n: (int)
        the number of pixels in the chain

    :param background: (:class:`~godafoss.color`)
        the background color (default: black)

    :param order: (str)
        the color order (default: RGB)    

    Neopixels are seperately controllable RGB LEDs,
    either as separate chip and LED, or as chip combined with an RGB LED.
    Neopixels can be connected into a chain, where only the first
    pixel is connected to a microcontroller.
    Power and data (and for some types a clock) are fed
    from each neopixel to the next.
    Such chains are often used in strips, and sometimes as rectanges
    (where the chain is folded).
    
    The common chip are summarized in the table below.
    The apa102 and ws2801 chips have dedicated driver classes.
    The hd107 seems to use the same protocol as the apa102, so
    it should work with that driver.
    The ws2811, ws2812, ws2813 and ws2815 chips 
    can use the ws281x driver class.
    
    +----------+-------+--------------+--------+------------------+
    | chip     | form  | interface    | power  | protocol         |
    +----------+-------+--------------+--------+------------------+
    | apa102   | chip  | data, clock  | 5V     | start, data, end |
    +----------+-------+--------------+--------+------------------+
    | hd107    | led   | data, clock  | 5V     | start, data, end |
    +----------+-------+--------------+--------+------------------+
    | ws2801   | chip  | data, clock  | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2811   | chip  | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2812   | led   | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2813   | led   | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2815   | led   | data         | 12V    | data only        |
    +----------+-------+--------------+--------+------------------+
    
    Be aware that a chain of neopixels can draw a significant amount of
    current: at for brightness 60mA per pixel.
    Hence for non-trivial amounts of neopixels a separate power supply 
    is required, and power + ground 'bypass' wiring might be needed.
    """

    # =======================================================================

    def __init__( 
        self,  
        n: int, 
        background, 
        order: str = "RGB"
    ):
        gf.canvas.__init__(
            self,
            size = gf.xy( n, 1 ),
            is_color = True,
            background = gf.colors.black
        )
        
        order = order.upper()
        if order == "RGB":
            self._permutate = lambda ink: ( ink.red, ink.green, ink.blue )
        elif order == "RBG":
            self._permutate = lambda ink: ( ink.red, ink.blue, ink.green )
        elif order == "BGR":
            self._permutate = lambda ink: ( ink.blue, ink.green, ink.red )
        elif order == "BRG":
            self._permutate = lambda ink: ( ink.blue, ink.red, ink.green )
        elif order == "GRB":
            self._permutate = lambda ink: ( ink.green, ink.red, ink.blue )
        elif order == "GBR":
            self._permutate = lambda ink: ( ink.green, ink.blue, ink.red )
        else:
            raise ValueError( "color order '%s'", order )
        

    # =======================================================================
    
    def _write_pixel_implementation( 
        self, 
        location: ( int, gf.xy ), 
        ink: gf.color
    ):      
        self._pixels[ location.x ] = self._permutate( ink )

    # =======================================================================
    
    def demo_color_wheel(
        self,
        color_list = (
            gf.colors.red,
            gf.colors.green,
            gf.colors.blue,
            gf.colors.white
        ),
        delay: int = 10_000,
        iterations = None,
        dim: int = 30
    ):
        for _ in gf.repeater( iterations ):
            for c in ( color_list ):
                self.clear()
                for n in range( self.size.x + 1 ):
                    self.flush()
                    gf.sleep_us( delay )
                    self.write_pixel(
                        gf.xy( n, 0 ),
                        c // dim
                    )  
                for n in range( self.size.x + 1 ):
                    self.flush()
                    gf.sleep_us( delay )
                    self.write_pixel(
                        gf.xy( n, 0 ),
                        gf.colors.black
                    ) 
    
# ===========================================================================
