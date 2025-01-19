import sys
import pathlib
sys.path.append( pathlib.Path(__file__).parent.parent.resolve() )
import godafoss
from godafoss.tests import test
test()

