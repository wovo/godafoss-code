# scipt that builds the package.json file

from os import listdir
from os.path import isfile, join

f = open( "package.json", "w" )
f.write( '{\n    "urls": [' )
mypath = "lib/godafoss"
c = ""
for name in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
    f.write( 
        '%s\n         ["godafoss/%s", "github:wovo/godafoss/lib/godafoss/%s"]' 
        % ( c, name, name ) )
    c = ","
f.write( '\n    ],\n    "version": "0.1"\n}\n' )
    
