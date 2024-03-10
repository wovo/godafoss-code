import godafoss as gf
edge = gf.edge()

gf.pcd8544(
    size = gf.xy( 84, 48 ),
    spi = edge.spi(),
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    background = False    
).demo()