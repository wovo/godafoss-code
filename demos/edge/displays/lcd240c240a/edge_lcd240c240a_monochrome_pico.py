import godafoss as gf
edge = gf.edge()

display = gf.lcd240c240a(
    spi = edge.spi( frequency = 20_000_000 ),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    monochrome = True,
    mechanism = 2
)

display.demo()


