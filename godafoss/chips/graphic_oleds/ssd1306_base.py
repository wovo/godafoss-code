# ===========================================================================
#
# file     : ssd1306_base.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
import framebuf

# ===========================================================================

class ssd1306_base( gf.canvas ):
    """    
    This is a driver for the ssd1306 monochrome oled display driver
    for up to 128x64 pixels.
    The driver implements the sheet interface.
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels    
    
    :param background: (bool)
        the default background pixel value    
    
    Oled modules with the ssd1306 chip are widely availavailable.
    Most have 128x64 pixels, but 128x32 and 70x40 can also be found.
    The 4-pin modules are i2c-only.
    The common 7-pin modules are spi, but can be reconfigured for i2c
    by resoldering some resistors.
    """

    # =======================================================================

    class commands:
        set_contrast        = const( 0x81 )
        set_entire_on       = const( 0xa4 )
        set_norm_inv        = const( 0xa6 )
        set_disp            = const( 0xae )
        set_mem_addr        = const( 0x20 )
        set_col_addr        = const( 0x21 )
        set_page_addr       = const( 0x22 )
        set_disp_start_line = const( 0x40 )
        set_seg_remap       = const( 0xa0 )
        set_mux_ratio       = const( 0xa8 )
        set_com_out_dir     = const( 0xc0 )
        set_disp_offset     = const( 0xd3 )
        set_com_pin_cfg     = const( 0xda )
        set_disp_clk_div    = const( 0xd5 )
        set_precharge       = const( 0xd9 )
        set_vcom_desel      = const( 0xdb )
        set_charge_pump     = const( 0x8d )

    # =======================================================================

    def __init__(
        self,
        size: xy,
        background: bool
    ) ->  None:

        canvas.__init__( 
            self, 
            size = size,
            is_color = False,
            background = background
        )
        self._buffer = bytearray((( self.size.y + 7 ) // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB )
            
        for x in (
            
            # disable
            self.commands.set_disp | 0x00,
            
            # resolution and layout
            self.commands.set_mem_addr, 0x00,  # horizontal
            self.commands.set_seg_remap | 0x01,  # column 127 = seg0
            self.commands.set_mux_ratio, self.size.y - 1,
            self.commands.set_com_out_dir | 0x08,  # scan from com[n] to com0
            self.commands.set_disp_offset, 0x00,
            self.commands.set_com_pin_cfg, 0x02 if self.size.y == 32 else 0x12,
            
            # timing and driving scheme
            self.commands.set_disp_clk_div, 0x80,
            self.commands.set_precharge, 0xf1,
            self.commands.set_vcom_desel, 0x30,  # 0.83*vcc
            self.commands.set_charge_pump, 0x14,
            
            # enable
            self.commands.set_contrast, 0xff,  # maximum
            self.commands.set_norm_inv | 0x00,
            self.commands.set_entire_on,             
            self.commands.set_disp | 0x01,

        ):
            self.write_command( x )
        
    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool
    ) -> None:
        self._framebuf.pixel(
            location.x,
            location.y,
            ink
        )           

    # =======================================================================
    
    def _clear_implementation(
        self,
        ink: bool
    ) -> None:
        self._framebuf.fill( 0xFF if ink else 0x00 )

    # =======================================================================

    def write_command(
        self,
        cmd: int
    ) -> None:
        """
        write a command byte to the chip
        """
        raise NotImplementedError
               
    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        
        # the active area is x-centered
        x0 = ( 128 - self.size.x ) // 2 
        x1 = x0 + self.size.x - 1
            
        self.write_command( self.commands.set_col_addr )
        self.write_command( x0 )
        self.write_command( x1 )
        self.write_command( self.commands.set_page_addr )
        self.write_command( 0 )
        self.write_command( ( self.size.y // 8 ) - 1 )
        self._write_framebuf()

    # =======================================================================
        
        
# ===========================================================================
