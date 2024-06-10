file = "../godafoss/index.html"

lines = []
for line in open( file, 'r', encoding="utf8" ).readlines():
    if line.startswith( '<dl class="py function">' ) or line.startswith( '<dl class="py class">' ):
        line = "<HR>" + line
    line = line.replace( '<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>', "" )
    lines.append( line )

f = open( file, 'w', encoding="utf8" )
for line in lines:
    f.write( line )
f.close()
    