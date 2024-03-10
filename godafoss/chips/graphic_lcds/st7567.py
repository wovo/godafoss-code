# ===========================================================================
#
# file     : gf_st7567.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

import framebuf
import machine

import godafoss as gf

SET_BIAS  =const(0xA2)
POWER_CTRL=const(0x28)
SET_BOOST =const(0xF8)
SOFT_RST  =const(0xE2)
SEG_DIR   =const(0xA0)
COM_DIR   =const(0xC0)
REGU_RATIO=const(0x20)
EVSET_MODE=const(0x81)
DISP_ONOFF=const(0xAE)
INV_DISP  =const(0xA6)#0:normal display 1:inverse
ALL_PIX_ON=const(0xA4)
SRTLIN_SET=const(0x40)#40~7F
PAGEAD_SET=const(0xB0)#b0~b8
COLHAD_SET=const(0x10)#0x10~0x1F
COLLAD_SET=const(0x00)#0x00~0x0F


# ===========================================================================

class st7567(
    gf.canvas,
    gf.lcd_spi,
    gf.lcd_reset_backlight_power
):
    
    def __init__( 
        self, 
        size, 
        spi, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: [ int, pin_out, pin_in_out, pin_oc ] = None,
        background = gf.colors.black, 
        invert = False,
        x_reverse = True,
        y_reverse = False,
        xy_swap = False,
        x_deadband = 0,
        elecvolt=0x1F,regratio=0x03,invX=0x01,invY=0x00,invdisp=0x00        
    ):
        gf.canvas.__init__(
            self,
            size = size,
            is_color = False,
            background = background
        )

        gf.lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
                    
        gf.lcd_reset_backlight_power.__init__( 
            self, 
            reset = gf.make_pin_out( reset ).inverted(),
            backlight = backlight, 
            power = power,          
            reset_duration = 10,
            reset_wait = 120_000
        )
        
        self._buffer = bytearray((( self.size.y + 7 ) // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB )
        
        self.EV=elecvolt
        self.RR=regratio
        self.invX=0x00 if(invX==0) else 0x01#0x00:MX=0 normal dir, 0x01:MX=1 reverse dir
        self.invY=0x00 if(invY==0) else 0x08#0x00:MY=0 0x08:MY=1
        self.invdisp=0x00 if(invdisp==0) else 0x01
        
        #self.EV=0x28
        if 1:
         self.write_command( [
            SOFT_RST, #optional, I think it's useless
            SET_BOOST, 0x00, #boost: 0x00:x4 0x01:x5
            SET_BIAS|0x01, # 0:1/9 1:1/7
            EVSET_MODE, self.EV, 
            REGU_RATIO|3, #0x00~0x07 3.0~6.5
            POWER_CTRL|0x07, # booster on,regulator on,follower on
            INV_DISP|self.invdisp, 
            ALL_PIX_ON|0x00, 
            SEG_DIR|self.invX,#0:MX=0 normal dir, 1:MX=1 reverse dir
            COM_DIR|self.invY, #0x00:MY=0 0x08:MY=1 (may change to reverse y)
        ] )
        
        if 0:
         self.write_command( 0xe2);
         self.write_command( 0x2c);
         self.write_command( 0x2e);
         self.write_command( 0x2f);
         self.write_command( 0x23);
         self.write_command( 0x81);
         self.write_command( 0x28);
         self.write_command( 0xa2);
         self.write_command( 0xc8);
         self.write_command( 0xa0);
         self.write_command( 0x40);
         self.write_command( 0xaf);        
        
        gf.sleep_us( 50_000 )
        self.write_command(DISP_ONOFF|0x01)#1:display on normal display mode        
                       
    # =======================================================================

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        
        self.write_command( SRTLIN_SET|0x00 )
        for pagcnt in range(8):
            self.write_command(
                ([PAGEAD_SET|pagcnt,COLHAD_SET|0x00,COLLAD_SET|0x00]),
                [ 0xAA, 0xAA, 0xAA, 0xAA ],
                buffer = self._buffer[(128*pagcnt):(128*pagcnt+128)]
            )
        return    
        
        #self.write_cmd(DISP_ONOFF|0x00)
        self.write_command(SRTLIN_SET|0x00)
        colcnt=0
        pagcnt=0
        while (pagcnt<9):
            self.write_command( [
                PAGEAD_SET|pagcnt,
                COLHAD_SET|0x00,
                COLLAD_SET|0x00
            ] )    
            if(pagcnt<8):
                self.write_command( None, buffer = self._buffer[(128*pagcnt):(128*pagcnt+128)])
            else:
                while (colcnt<128):
                    colcnt+=1
                    self.write_command(None, b"\x00")
            pagcnt+=1
        #self.write_cmd(DISP_ONOFF|0x01)                
        
    # =======================================================================
        
    def _clear_implementation( 
        self,
        ink: bool
    ):
        self._framebuf.fill( 0xFF if ink else 0x00 )     
        
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
    
# ===========================================================================
 