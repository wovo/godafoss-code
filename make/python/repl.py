import serial

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch()
        else:
            return None        


getch = _Getch()

serial_port_name = "COM42"

port = serial.Serial( 
    serial_port_name, 
    baudrate = 115200,
    timeout = 0.01
)

while True:
    c = getch()
    if c is not None:
        port.write( c )
              
    c = port.read( 1 )
    if len( c ) > 0:
        c = c.decode( "utf-8" )
        print( c, end = "" )
    