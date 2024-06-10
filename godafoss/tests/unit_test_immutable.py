# ===========================================================================
#
# file     : unit_test_immutable.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class frozen( gf.immutable ):

    def __init__( self ):
        self.x = 5
        self.y = 9
        del self.y
        gf.immutable.__init__( self )


# ===========================================================================

def unit_test_immutable():
    print( "test immutable" )

    fr = frozen()
    assert fr.x == 5

    try:
        fr.x = 9
        assert False
    except:
        pass

    try:
        fr.y = 9
        assert False
    except:
        pass

    try:
        del fr.x
        assert False
    except:
        pass

    # immutable example
    import godafoss as gf
    class im( gf.immutable ):
        def __init__( self ):
            self.x = 5
            gf.immutable.__init__( self )
    #
    assert im().x == 5
    try:
        im().x = 6
        assert False
    except:
        pass


# ===========================================================================
