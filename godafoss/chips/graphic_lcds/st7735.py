# ===========================================================================
#
# file     : gf_st7735.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

# $$document( 0 )

import godafoss as gf


# ===========================================================================

class st7735( gf.glcd ):

    # =======================================================================

    class cmd:
        NOP     = gf.const( 0x00 ) 
        SWRESET = gf.const( 0x01 )
        RDDID   = gf.const( 0x04 )
        RDDST   = gf.const( 0x09 )
        
        SLPIN   = gf.const( 0x10 )
        SLPOUT  = gf.const( 0x11 )
        NORON   = gf.const( 0x13 )        
        INVOFF  = gf.const( 0x20 )
        INVON   = gf.const( 0x21 )
        DISPOFF = gf.const( 0x28 )
        DISPON  = gf.const( 0x29 )
        
        CASET   = gf.const( 0x2A )
        RASET   = gf.const( 0x2B )
        RAMWR   = gf.const( 0x2C )
        RAMRD   = gf.const( 0x2E )
        PTLAR   = gf.const( 0x30 )
        COLMOD  = gf.const( 0x3A )
        MADCTL  = gf.const( 0x36 )
        RDID1   = gf.const( 0xDA )
        RDID2   = gf.const( 0xDB )
        RDID3   = gf.const( 0xDC ) 
        RDID4   = gf.const( 0xDD ) 
        FRMCTR1 = gf.const( 0xB1 ) 
        FRMCTR2 = gf.const( 0xB2 )
        FRMCTR3 = gf.const( 0xB3 )
        INVCTR  = gf.const( 0xB4 )
        PWCTR1  = gf.const( 0xC0 )
        PWCTR2  = gf.const( 0xC1 )
        PWCTR3  = gf.const( 0xC2 )
        PWCTR4  = gf.const( 0xC3 )
        PWCTR5  = gf.const( 0xC4 )
        VMCTR1  = gf.const( 0xC5 )
        GMCTRP1 = gf.const( 0xE0 )
        GMCTRN1 = gf.const( 0xE1 )

    # =======================================================================

    def __init__( 
        self, 
        *args, **kwargs
    ):
        gf.glcd.__init__( self, *args, **kwargs )

        """
        self.write_command( self.cmd.PWCTR1 )
        self.write_command( self.cmd.PWCTR2, [ 0xC0 ] )
        self.write_command( self.cmd.PWCTR3, [ 0x0D, 0x00 ] )
        self.write_command( self.cmd.PWCTR4, [ 0x8D, 0x6A ] )
        self.write_command( self.cmd.PWCTR5, [ 0x8D, 0xEE ] )

        self.write_command( self.cmd.VMCTR1, [ 0x0E ] )

        self.write_command( self.cmd.GMCTRP1,
            [ 0x10, 0x0E, 0x02, 0x03, 0x0E, 0x07, 0x02, 0x07,
              0x0A, 0x12, 0x27, 0x37, 0x00, 0x0D, 0x0E, 0x10 ] )
        self.write_command( self.cmd.GMCTRN1,
            [ 0x10, 0x0E, 0x03, 0x03, 0x0F, 0x06, 0x02, 0x08,
              0x0A, 0x13, 0x26, 0x36, 0x00, 0x0D, 0x0E, 0x10 ] )
        
        self.write_command( self.cmd.FRMCTR1,
            [ 0x05, 0x3A, 0x3A ] )
        self.write_command( self.cmd.FRMCTR2,
            [ 0x05, 0x3A, 0x3A ] )
        self.write_command( self.cmd.FRMCTR3,
            [ 0x05, 0x3A, 0x3A, 0x05, 0x3A, 0x3A ] )
        """
        
    # =======================================================================

# ===========================================================================
