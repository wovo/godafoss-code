if 1:
    from machine import SPI
    from random import randint
    import godafoss as gf

    eink = gf.badger2040()
    eink.display.clear()
    
    s = eink.display
    for _ in gf.repeater( 0 ):

        if 1:
            s.write( gf.rectangle( s.size ) )
            s.flush()
            
        s.write( gf.text( "Hello worl!" ), gf.xy( 10, 10 ) )            

        if 0:
         for dummy in range( 0, 10 ):
            start = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            end = gf.xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( gf.rectangle( end - start ) @ start )
    
    s.write( gf.rectangle( gf.xy( 120, 11 ) ) @ gf.xy( 0, 0 ) )
    s.write( gf.text( "Hello world !" ), gf.xy( 1, 2 ) )            
    eink.display.flush()

