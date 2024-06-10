# ===========================================================================
#
# file     : make_documentation.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2022
# license  : MIT license
#
# This script gathers and processes the source files into a single
# __init__.py file, to be processed by sphinx, to generate the html 
# and/or pdf version of the documentation.
# This script should be run from the root of the repository.
#
# For running the tests and generating the documentation the
# dependencies are:
#   - sphinx
#   - rst2pdf 
#
# ToDo
# - have blink accept any as_pin_out pin, or make_pin_out that also accepts a number
# - use same for ports
# - images repository
# - expand start page
# - target pinouts
# - now no white line in pdf
# - ports doen't show the methods inhertited from _port
# - port documentation
# - pin documentation -> visible pin_base
# - pdf image is too small, half the image for html, generate?
# - weird pdf errors
# - servo examples
# - canvas examples
# - separate module with the target boards and pinouts?
# - hd44780 test
# - hd44780 bliking demo (and more?)
# - hd44780 pictures
# - pcd8544 shows weird parameter types
# - __init__ parameters are still shown in the class header
# - no def for function definitions?
# - skip init without args
# https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
# - don't use init & repr for documentation?
#
# ===========================================================================

import os, sys, shutil, glob
from PIL import Image
import sys
sys.path.append( "godafoss" )


# ===========================================================================

def _inline_example( name: str, lines: str = None, image = True ):

    """the docstring part for an example
    """
    
    result = ""

    if image:
        result += f"""

.. only:: html

   .. image::  ../examples/images/{name}_html.png

.. only:: pdf

    .. image::  ../examples/images/{name}_pdf.png

"""

    if lines is not None:
        result += f"""

.. literalinclude:: ../examples/{name}.py
    :lines: {lines}

"""
    return result
    
    
# ===========================================================================

def bar( s, n ):
    return "" if n < 1 else s + bar( s, n - 1 )


# ===========================================================================

def insert_example( file, marker, spaces ):
    f = open( "test/native/" + file, "r" )
    result = []
    gather = False
    found = False
    b = bar( " ", 4 * ( spaces + 1 ))
    for line in f:
        if gather:
            if line.strip() == "":
                result.append( "\n" )        
                gather = False
            elif line.strip().startswith( 'equal(' ) \
             or line.strip().startswith( 'close(' ):
                t = eval( line.replace( 'equal', '' ).\
                    replace( 'close', '' ) )
                s = b + t[ 0 ] + " -> " + t[ 1 ] + "\n"
                s = s.replace( "\\", "\\\\" )
                result.append( s )
            else:
                if line == "#\n":
                    line = "\n"
                result.append( b + line )            
        if line.find( marker ) > -1:
            gather = True
            found = True
            result.append( "\n" )
    f.close()
    if gather:
        result.append( "\n" )   
    if not found:
        print( "example not found: %s %s" % ( file, marker ))
    return result
    
def make_image( name, postfix, new_width ):
    im = Image.open( "../godafoss-pics/images/" + name + ".png")
    if new_width is None:
        new_width = im.width 
    new_size = ( new_width, ( im.height * new_width ) // im.width ) 
    resized = im.resize( new_size )
    resized.save( "tempdir/" + name + postfix + ".png" )
    resized.close()
    im.close()  
    
    
# ===========================================================================

def insert_image( 
    name, 
    level, 
    html_width = None, 
    pdf_width = None,
    width = None
    
):
    s = " " * 4 * level
    result = \
"""
 
@.. only:: html

@   .. image::  ../../tempdir/%s_html.png
@       $width

@.. only:: pdf

@    .. image::  ../../tempdir/%s_pdf.png
@       $width

"""
    result = result.replace( "@", s ) % ( name, name )
    result = result.replace( "$width",
        "" if width is None else ":width: %d %% " % width )

    if pdf_width is None:
        if html_width is not None:
            pdf_width = html_width * 2
            
    try:        
        make_image( name, "_html", html_width )            ,
        make_image( name, "_pdf", pdf_width )            ,
    except FileNotFoundError:
        print( "image not found: %s" % name )
        return "missing image %s" % name       

    return result
   
   
# ===========================================================================

def find_source_files( path ):
    results = []
    for entry in os.listdir( path ):
        # < 1 to keep __init__.py
        if entry.endswith( ".py" ) \
            and ( entry.find( "__" ) < 1 ):
            results.append( path + "/" + entry )
        elif ( entry.find( "." ) < 0 ) \
            and ( entry != "tests" ):
            results += find_source_files( path + "/" + entry )
    return results    
   
   
# =========================================================================== 

def is_name_char( c ):
    return c.isalnum() or c == "_"

def dependencies( file ):
    result = []
    for line in open( file ).readlines():
        while line.find( " gf." ) > -1:
            line = line[ 4 + line.find( " gf." ) : ]
            name = ""
            while is_name_char( line[ 0 ] ):
                name += line[ 0 ]
                line = line[ 1 : ]
            if ( not name in result ) \
                and (
                    ( line[ 0 ] != "(" )
                    or ( name == "clamp" )
                ):
                result.append( name )
    print( file, result )
    return result   


# =========================================================================== 

def dependency_file_name( file, file_list ):
    for x in file_list:
        if x.find( "/" + file + ".py" ) > -1:
            return x
    return dependency_file_name( "__init__", file_list )
        

# =========================================================================== 

def add_file( file, file_list, sorted_files ):
    if not file in sorted_files:
        for dep in dependencies( file ):
            full_name = dependency_file_name( dep, file_list )
            add_file( full_name, file_list, sorted_files )
        sorted_files.append( file )            

        
# =========================================================================== 

def sorted_source_files( path ):
    file_list = find_source_files( path )
    sorted_files = [ 
        "godafoss/docs/intro.py", 
        "godafoss/tools/always.py", 
    ]
    for file in file_list:
        if (
        not file in [
            "godafoss/__init__mpy.py",
        ] 
        and not file.find( "__" ) > -1
        ):
            add_file( file, file_list, sorted_files )
    xsorted_files = [
        file for file in sorted_files
        if file in [
            "godafoss/tools/intro.py"        ,
            "godafoss/__init__.py",
        ]
    ]    
    return sorted_files        
        

# ===========================================================================

def make_documentation():  
    make_html = False
    make_pdf = False

    for arg in sys.argv[ 1: ]:
        if arg == "all":
            make_pdf = True
            make_html = True
       
        elif arg == "pdf":
            make_pdf = True
       
        elif arg == "html":
            make_html = True
       
        else:
            raise Exception( "unknown argument '{arg}'", arg )
        
    if not os.path.isfile( "make/sphinx/prepare_documentation.py" ):
        raise Exception( "must be run from the root" )    
        
    try:
        shutil.rmtree( "tempdir" )
    except:
        pass
    try:
        os.makedirs( "tempdir/godafoss" )
    except:
        pass
        
    lines = []
    macros = {}
    for file_name in sorted_source_files( "godafoss" ):
     if not file_name in []:
        lines.append( f"\n#=> {file_name}\n\n" )
        docstring = ""
        gather = False
        macro_name = None
        nr = 0
        leftover = ""
        insert_at_blank = None
        input = list( open( file_name, "r" ).readlines() )
        while len( input ) > 0:
            line = input[ 0 ]
            input = input[ 1 : ]
            nr += 1
            #print( nr, line )
            
            if line.rstrip().endswith( "\\" ):
                line = line.rstrip()
                if leftover != "":
                    line = line.lstrip()  
                leftover += line[ : -2 ]
                continue
            if leftover != "":
                line = line.lstrip()    
            line = leftover + line
            leftover = ""
        
            if gather:
                docstring += line
                if False and line.replace( "\n", "" ).strip().endswith( '"""' ):
                    #print( docstring )
                    try:
                        docstring = eval( f'f{docstring.strip()}' )
                    except:
                        print( "ERROR", docstring )    
                    lines.append( start + docstring + '"""\n')
                    docstring = ""
                    gather = False
                    
            elif False and line.strip().startswith( '"""' ):
                start = line
                docstring += line
                gather = True
                
            elif ( macro_name is None ) and line.strip().startswith( '$macro_insert' ):
                name = line.split( "$macro_insert" )[ 1 ].split( " " )[ 1 ].strip()
                prefix = line.split( "$" )[ 0 ]
                arguments = line.split( name )[ 1 ].strip().split( " " )
                #print( name, line, arguments )
                try:
                    m = macros[ name ]
                except:
                    m = []
                    print( "unknown macro %s:%d '%s'" % ( file_name, nr, name ) )                    
                for x in reversed( m ):
                    j = 0
                    for r in arguments:
                        j += 1
                        x = x.replace( "$%d" % j, r )                   
                    input = [ prefix + x ] + input                
                    
            elif ( macro_name is None ) and line.find( '$macro_insert' ) > 0:
                split = line.strip().split( '$macro_insert', 1 )
                name = split[ 1 ].strip().split( ' ', 1 )[ 0 ].strip( ")" )
                s = ''
                try:
                    m = macros[ name ]
                except:
                    m = []
                    print( "unknown macro %s:%d '%s'" % ( file_name, nr, name ) )
                for x in m:
                    s += x.replace( "\n", ' ' )
                lines.append( 
                    line.replace( name, '' ).replace( '$macro_insert', s )
                )
                
            elif line.strip().startswith( '$macro_start' ):
                macro_name = line.split( "$macro_start" )[ 1 ].strip()
                macro_prefix = line.split( "$" )[ 0 ]
                macro_lines = []
                
            elif line.strip().startswith( '$macro_end' ):    
                macros[ macro_name ] = macro_lines
                macro_name = None
                
            elif line.strip().startswith( '"$methods"' ):   
                print( f"=============== $methods {file_name}" )    
                # name = file_name.                
                for f in glob.glob( file_name.replace( ".py", "__*.py" ) ):
                     for l in open( f ).readlines():
                         #if l.find( "import godafoss as gf" ) < 0:
                         l = l.replace( file_name.replace( ".py", "" ) + "__", "" )
                         lines.append( ( line.find( '"$methods"' ) * " " ) + l )
                
#            elif line.strip().startswith( "import godafoss as gf" ):
#                pass

            elif line.strip().startswith( "from godafoss." ):
                pass

            elif macro_name is not None:
                macro_lines.append( line.replace( macro_prefix, "", 1 ) )

            elif line.strip().startswith( '$' ):
                line = line.replace( '$', '', 1 )
                try:
                    s = eval( line )
                except Exception as error:
                    print( "%s %s:%d" % ( error, file_name, nr ) )
                    s = []
                for line in s:
                    lines.append( line )
                
            else:             
                i = line.find( "#=> " )            
                if i > -1:
                    line = line.replace( "#=> ", "" )    
                    insert_at_blank = i * " " + "    pass\n"    

                if ( insert_at_blank is not None ) \
                    and ( line.replace( "\n", "" ).strip() == "\n" ):
                    # this never happens, 
                    # but doesn't seem to be needed anyway
                    lines.append( insert_at_blank )
                    insert_at_blank = None

                lines.append( line )
       
    with open( "tempdir/godafoss/__init__.py", "w" ) as file:
        for line in lines:
            file.write( line )  
    
    """
    # add the files that must be mocked for running with normal python
    for f in ( 
        "machine.py", 
        "framebuf.py", 
        "micropython.py",  
    ):
        shutil.copy( "test/native/" + f, "tempdir/" + f )
    for f in ( 
        "gf_gc.py", 
        "gf_time.py" 
    ):
        shutil.copy( "test/native/" + f, "tempdir/godafoss/" + f )
    """    
    
    """
    if make_html:
        os.system( "sphinx-build -E -a -b html sphinx html" )
        # os.system( "cmd -C make_html.bat" )
       
    if make_pdf:
        os.system( "sphinx-build -t pdf -b pdf sphinx pdf" )
    """
    
make_documentation()       