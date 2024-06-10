import glob
import shutil

for entry in glob.glob( "godafoss/**/__pycache__", recursive = True ):
    shutil.rmtree( entry )
 
