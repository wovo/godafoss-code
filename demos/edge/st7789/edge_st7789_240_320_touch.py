import godafoss as gf
import edge

import time
import edge

spi = edge.soft_spi()
# spi = edge.hard_spi( 1, 1_000_000 )
   
t = gf.xpt2046(
    spi = spi,
    cs = edge.p7,
    size = gf.xy( 1000, 1000 )
)

t.demo()


