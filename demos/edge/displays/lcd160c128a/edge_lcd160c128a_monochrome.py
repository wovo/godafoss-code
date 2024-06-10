import godafoss as gf
edge = gf.edge()

display = gf.lcd160c128a(
    spi = edge.spi( frequency = 20_000_000 ),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    monochrome = True
)

display.demo()


