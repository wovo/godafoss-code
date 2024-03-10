import godafoss as gf
import edge

spi = edge.soft_spi()

mrf = gf.mrfc522(
    spi = spi,
    rst = edge.p4,
    cs = edge.p3
    )
mrf.demo()