import godafoss as gf
board = gf.board_luatos_core_esp32c3()
button = board.button

gf.make_pin_in( button ).demo()


