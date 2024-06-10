import godafoss as gf
edge = gf.edge()

display = gf.lcd160c80a(
    spi = edge.spi( frequency = 20_000_000 ),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight
)

python = gf.ggf( "python_125_128.ggf" )

display.clear()
display.write( python )
display.flush()