import godafoss as gf
board = gf.board_luatos_core_esp32c3()
display = board.air101_display()
cursor = board.air101_cursor()

size = 5
location = display.size // 2
circles = []
while True:
    # gf.sleep_us( 10_000 )
    location = location + 2 * cursor.direction()
    display.clear( gf.colors.green )
    for c in circles:
        gf.circle( 2 * size ).write( display, c, gf.colors.black )
    if cursor.down() and not location in circles:
        circles.append( location )
    gf.circle( size, fill = True ).write( display, location, gf.colors.red )
    display.flush()


