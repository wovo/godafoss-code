import sys
sys.path.insert( 1, "..\\..\\.." )

import godafoss as gf
edge = gf.edge()

gf.blink( edge.port_out() )
