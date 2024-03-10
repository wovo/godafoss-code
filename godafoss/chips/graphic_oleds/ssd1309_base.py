# ===========================================================================
#
# file     : gf_ssd1309_base.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

from micropython import const
import machine
import framebuf

import godafoss as gf


# ===========================================================================

class ssd1309_base( gf.canvas ):
    """
    ssd1309 spi/i2c b/w oled display driver
    """

    # Command constants from display datasheet
    CONTRAST_CONTROL = const(0x81)
    ENTIRE_DISPLAY_ON = const(0xA4)
    ALL_PIXELS_ON = const(0XA5)
    INVERSION_OFF = const(0xA6)
    INVERSION_ON = const(0XA7)
    DISPLAY_OFF = const(0xAE)
    DISPLAY_ON = const(0XAF)
    NOP = const(0xE3)
    COMMAND_LOCK = const(0xFD)
    CHARGE_PUMP = const(0x8D)

    # Scrolling commands
    CH_SCROLL_SETUP_RIGHT = const(0x26)
    CH_SCROLL_SETUP_LEFT = const(0x27)
    CV_SCROLL_SETUP_RIGHT = const(0x29)
    CV_SCROLL_SETUP_LEFT = const(0x2A)
    DEACTIVATE_SCROLL = const(0x2E)
    ACTIVATE_SCROLL = const(0x2F)
    VSCROLL_AREA = const(0xA3)
    SCROLL_SETUP_LEFT = const(0x2C)
    SCROLL_SETUP_RIGHT = const(0x2D)

    # Addressing commands
    LOW_CSA_IN_PAM = const(0x00)
    HIGH_CSA_IN_PAM = const(0x10)
    MEMORY_ADDRESSING_MODE = const(0x20)
    COLUMN_ADDRESS = const(0x21)
    PAGE_ADDRESS  = const(0x22)
    PSA_IN_PAM = const(0xB0)
    DISPLAY_START_LINE = const(0x40)
    SEGMENT_MAP_REMAP  = const(0xA0)
    SEGMENT_MAP_FLIPPED = const(0xA1)
    MUX_RATIO = const(0xA8)
    COM_OUTPUT_NORMAL = const(0xC0)
    COM_OUTPUT_FLIPPED = const(0xC8)
    DISPLAY_OFFSET = const(0xD3)
    COM_PINS_HW_CFG = const(0xDA)
    GPIO = const(0xDC)

    # Timing and driving scheme commands
    DISPLAY_CLOCK_DIV = const(0xd5)
    PRECHARGE_PERIOD = const(0xd9)
    VCOM_DESELECT_LEVEL = const(0xdb)
    
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

    def __init__(
        self,
        size: gf.xy,
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
                    
        for cmd in (
            self.DISPLAY_OFF, 
            self.DISPLAY_CLOCK_DIV, 0x80,
            self.MUX_RATIO, self.size.y - 1,
            self.DISPLAY_OFFSET, 0x00,
            self.DISPLAY_START_LINE,
            self.CHARGE_PUMP, 0x14,
            self.MEMORY_ADDRESSING_MODE, 0x00, 
            self.SEGMENT_MAP_FLIPPED,
            self.COM_OUTPUT_FLIPPED,
            self.COM_PINS_HW_CFG, 0x02 if (self.size.y == 32 or self.size.y == 16) and (self.size.x != 64)
                else 0x12,
            self.CONTRAST_CONTROL, 0xFF,
            self.PRECHARGE_PERIOD, 0xF1,
            self. VCOM_DESELECT_LEVEL, 0x40,            
            self.ENTIRE_DISPLAY_ON, # output follows RAM contents
            self.INVERSION_OFF, # not inverted
            self.DISPLAY_ON
        ):
            self.write_command(cmd) 
           
        self.clear()
        self.flush()
        
    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: gf.xy,
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
        ink
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

    def _flush_implementation( self, forced ) -> None:
        
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
