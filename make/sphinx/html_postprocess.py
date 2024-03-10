file = "docs/index.html"

lines = []
for line in open( file, 'r', encoding="utf8" ).readlines():
    if line.startswith( '<dl class="py function">' ) or line.startswith( '<dl class="py class">' ):
        line = "<HR>" + line
    lines.append( line )

f = open( file, 'w', encoding="utf8" )
for line in lines:
    f.write( line )
f.close()
    