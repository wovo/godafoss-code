import godafoss as gf

lcd = gf.ks0107(
    data = ( 0, 1, 2, 3, 4, 5, 6, 7 ),
    cs1 = 8,
    cs2 = 9,
    reset = 10,
    wr = 11,
    cd = 12,
    enable = 13  
)

lcd.demo()