# ===========================================================================
#
# file     : st7789.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# $$document( 0 )

import godafoss as gf


# ===========================================================================

class st7789b(
    gf.glcd,
):

#    gf.lcd_base
    
    class cmd: # klopt van geen kanten
        NOP        = gf.const( 0x00 )
        SWRESET    = gf.const( 0x01 )
        RDDID      = gf.const( 0x04 )
        RDDST      = gf.const( 0x09 )
        
        RDDPM      = gf.const( 0x0A )
        RDDMADCTL  = gf.const( 0x0B )
        RDDIM      = gf.const( 0x0D )
        RDDSEM     = gf.const( 0x0E )
        RDDSDR     = gf.const( 0x0F )
        SLPIN      = gf.const( 0x10 )
        SLPOUT     = gf.const( 0x11 )
        PTLON      = gf.const( 0x12 )
        NORON      = gf.const( 0x13 )
        INVOFF     = gf.const( 0x20 )
        INVON      = gf.const( 0x21 )
        GAMSET     = gf.const( 0x26 )
        DISPOFF    = gf.const( 0x28 )
        DISPON     = gf.const( 0x29 )
        CASET      = gf.const( 0x2A )
        RASET      = gf.const( 0x2B )
        RAMWR      = gf.const( 0x2C )
        RAMRD      = gf.const( 0x2E )
        PTLAR      = gf.const( 0x30 )
        VSCRDEF    = gf.const( 0x33 )
        TEOFF      = gf.const( 0x34 )
        TEON       = gf.const( 0x35 )
        MADCTL     = gf.const( 0x36 )
        COLMOD     = gf.const( 0x3A )

    def __init__( 
        self, 
        *args, **kwargs
    ):
        #gf.lcd_base.__init__( self, *args, **kwargs )        
        gf.glcd.__init__( self, *args, **kwargs )
        
        return

        #self.write_command( self.cmd.SWRESET )
        self.write_command( self.cmd.SLPOUT )
        gf.sleep_us(120_000)        
           
        self.write_command( self.cmd.COLMOD, [ 0x05 ] ) # was 66
        gf.sleep_us(120_000)  
      
        self.write_command( self.cmd.MADCTL, [ 0x10 ] );  # was 10                    
        self.write_command( self.cmd.CASET, [
            0, 0, self.size.x >> 8, self.size.x & 0xFF ])
        self.write_command( self.cmd.RASET, [
            0, 0, self.size.y >> 8, self.size.y & 0xFF ])
      
        #self.write_command( self.cmd.INVON )
        #time.sleep_ms( 10 )
        #self.write_command( self.cmd.NORON )
        #time.sleep_ms( 100 )
        #self.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
        
        #self.write_command(
        #    self.cmd.INVON if self._invert else self.cmd.INVOFF )  
        
        m = 0x00
        if self._swap_xy:
            m |= 0x20
        if self._mirror_x:
            m |= 0x40
        if self._mirror_y:
            m |= 0x80
        #self.write_command( self.cmd.MADCTL, [ m ] )          

        #self.write_command( self.cmd.NORON )
        #time.sleep_ms( 10 )

        #self.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
                   
    # =======================================================================

# ===========================================================================