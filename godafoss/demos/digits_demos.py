# ===========================================================================
#
# file     : digits_demos.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf


# ===========================================================================

def digits_demos(
    self,
    iterations = None
):
    """
    seven-segment digits display demo
    """

    print( "seven segments demo" )

    for _ in repeater( iterations ):

        for i in range( self.n ):
            for n in range( 10 ):
                for d in range( self.n ):
                    self.write(
                        ( " " * i ) + "%d" % n,
                        align = False
                    )
                    sleep_us( 10_000 )

        for i in range( 0, 10 ** self.n ):
            x = ( i // 100 ) % self.n
            self.write(
                "%d" % i,
                points = [ n == x for n in range( self.n ) ]
            )


# ===========================================================================
