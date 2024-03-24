# ===========================================================================
#
# file     : unit_test_no_new_attributes.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

class no_new( gf.no_new_attributes ):

    def __init__( self ):
        self.x = 5
        gf.no_new_attributes.__init__( self )


# ===========================================================================

def unit_test_no_new_attributes():
    print( "test no_new_attributes" )

    nn = no_new()
    assert nn.x == 5
    nn.x = 42
    assert nn.x == 42

    try:
        nn.y = 9
        assert False
    except:
        pass

    # no_new_attributes example
    import godafoss as gf
    class im( gf.no_new_attributes ):
        def __init__( self ):
            self.complicated_name = 5
            gf.no_new_attributes.__init__( self )
    #
    im().complicated_name = 42
    try:
        im().complikated_name = 42
        assert False
    except:
        pass


# ===========================================================================
