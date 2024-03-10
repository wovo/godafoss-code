import mpy_cross
import sys
import os
import glob
import shutil
from distutils.dir_util import copy_tree

def system( s ):
    print( "system:", s )
    os.system( s )

target = sys.argv[ 1 ]
if not target in [ "rp2040", "esp32" ]:
    print( "unknown target" )
    exit()
    
system( r"make/load/load_%s" % target )

