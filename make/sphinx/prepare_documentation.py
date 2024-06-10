# ===========================================================================
#
# file     : prepare_documentation.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2022
# license  : MIT license
#
# ===========================================================================
#
# Gather and processes the source files into a single
# __init__.py file, to be processed by sphinx, to generate the html 
# and/or pdf version of the documentation.
# Must be run from the root of the repository.
#
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
#
# ===========================================================================

import os, shutil, glob
from PIL import Image

import sys
sys.path.append( "." )
import godafoss


# ===========================================================================
#
# find the sources files that must be processed
#
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

# =========================================================================== 

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
    #print( file, result )
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
        "godafoss/tools/enums.py", 
]
    
    for file in file_list:
        if (
        not file in [
            "godafoss/__init__mpy.py",
        ] 
        and not file.find( "__" ) > -1
        ):
            add_file( file, file_list, sorted_files )
            
    return sorted_files  
    
# =========================================================================== 
#
# report an error for the specified line 
#
# =========================================================================== 

class report:
    def __init__( 
        self, 
        file_name, 
        nr, 
        line 
    ):
        self.file_name = file_name
        self.nr = nr
        self.line = line        
        
    def report(
        self,
        message 
    ):    
        print( f"[{self.file_name}:{self.nr}] {message}" )

# ===========================================================================
#
# return an embedded command of the format $$<name>( <parameters> )
#
# ===========================================================================

def embedded_command( 
    reporter, 
    line, 
    commands = None 
):
    marker = line.find( "$$" )
    if marker < 0:
        return None, None
        
    interesting = line[ marker : ]    
    
    start = interesting.find( "(" )
    if start < 0:
        reporter.report( "missing (" )
        return None, None

    end = interesting.find( ")" )
    if end < 0:
        reporter.report( "missing )" )    
        return None, None
        
    command = interesting[ 2 : start ]
    if not ( ( command in commands ) or ( commands == None ) ):
        return None, None    
    
    parameters = interesting[ start + 1 : end - 1 ]
    return command, parameters    

# ===========================================================================
#
# handle images
#
# ===========================================================================

def make_image( name, file_name, new_width ):
    im = Image.open( "../godafoss-pics/images/" + name + ".png")
    if new_width is None:
        new_width = im.width 
    new_size = ( new_width, ( im.height * new_width ) // im.width ) 
    resized = im.resize( new_size )
    resized.save( f"tempdir/{file_name}.png" )
    resized.close()
    im.close()  

# ===========================================================================

"""
.. list-table:: 
    * - $$insert_image( "lilygo_ttgo_t_dongle_s3_python", 200, "lilygo_ttgo_t_dongle_s3", "#godafoss.board_lilygo_ttgo_t_dongle_s3" )    
      - $$insert_image( "lilygo_ttgo_t_display", 200, "lilygo_ttgo_t_display", "#godafoss.board_lilygo_ttgo_t_display" )  
      - $$insert_image( "lilygo_ttgo_t_display", 200, "lilygo_ttgo_t_display", "#godafoss.board_lilygo_ttgo_t_display" )  
    * - $$insert_image( "lilygo_ttgo_t_dongle_s3_python", 200, "lilygo_ttgo_t_dongle_s3", "#godafoss.board_lilygo_ttgo_t_dongle_s3" )    
      - $$insert_image( "lilygo_ttgo_t_display", 200, "lilygo_ttgo_t_display", "#godafoss.board_lilygo_ttgo_t_display" )   
      - $$insert_image( "lilygo_ttgo_t_display", 200, "lilygo_ttgo_t_display", "#godafoss.board_lilygo_ttgo_t_display" ) 
"""

tables = { 
    "boards": [], 
    "displays": [] 
}

def add_table( table, name, image ):
    tables[ table ].append( [ name, image ] )

def insert_table( table, columns ):
    result = []
    result.append( ".. list-table:: \n" )
    pixels = [ None, 800, 400, 300, 200 ][ columns ]
    n = 0
    for name, image in tables[ table ]:
    
        n += 1
        if ( columns == 1 ) or ( n % columns == 1 ):
            s = "   * - "
        else:
            s = "     - "
            
        result.append( insert_image( 
            s, 
            image, 
            pixels, 
            name, 
            f"#godafoss.{name}" 
        ) )
        
    while n % columns != 0:
        n += 1
        result.append( "\n" )
        result.append( "     - \n" )
        result.append( "\n" )
        
    return result        

# ===========================================================================

def insert_image0( 
    prefix,
    name, 
    width,
    caption = "",
    link = None
    
):
    file_name = f"{name}_{width}"
    tabfix = " " * len( prefix )
    if ( link is None ) and ( caption == "" ):
        kind = "image"
    else:
        kind = "figure"
    
    if link == None:
        link = ""
    else:
        if caption != "":
            caption = f"`{caption} <{link}>`_"     
        link = f":target: {link}"
        
    try:        
        make_image( name, file_name, width )      

    except FileNotFoundError:
        print( "image not found: %s" % name )
        return "missing image %s" % name          
        
    return \
f"""

{prefix}.. {kind}::  ../../tempdir/{file_name}.png
{tabfix}    {link}

{tabfix}    {caption}

"""

    return result
    
def insert_image( 
    prefix,
    name, 
    width,
    caption = "",
    link = None
    
):
    file_name = f"{name}_{width}"
    tabfix = " " * len( prefix )
    if ( link is None ) and ( caption == "" ):
        kind = "image"
    else:
        kind = "figure"
    
    if link is not None:
        if caption != "":
            caption = f"`{caption} <{link}>`_"     
        link = f":target: {link}"
        
    try:        
        make_image( name, file_name, width )      

    except FileNotFoundError:
        print( "image not found: %s" % name )
        return "missing image %s" % name          
        
    result = f"\n{prefix}.. {kind}::  ../../tempdir/{file_name}.png\n"
    
    if link is not None:
        result += f"{tabfix}    {link}\n"
        
    if caption != "":
        result += f"\n{tabfix}    {caption}\n"

    return result + "\n"


# ===========================================================================

def see_also( 
    prefix,
    *args
):
    result = f"{prefix}see also: "
    separator = ""
    for arg in args:
        result += ref( separator, arg )[:-1]
        separator = ", "
    return result + "\n"

    
# ===========================================================================

def insert_example(
    prefix,
    file_name,
    marker,
    spaces
):    
    f = open( "godafoss/" + file_name, "r" )
    result = []
    gather = False
    found = False
    #b = bar( " ", 4 * ( spaces + 1 ))
    for line in f:
        if gather:
            if line.strip() == "":
                result.append( "\n" )        
                gather = False
            elif line.strip().startswith( 'assert ' ) \
             or line.strip().startswith( 'close(' ):
                t = eval( line.replace( 'assert ', ' ' ).\
                    replace( 'close', '' ) )
                s = prefix + t[ 0 ] + " -> " + t[ 1 ] + "\n"
                s = s.replace( "\\", "\\\\" )
                result.append( s + "\n" )
            else:
                if line == "#\n":
                    line = "\n"
                result.append( prefix + line + "\n" )            
        if line.find( marker ) > -1:
            gather = True
            found = True
            result.append( "\n" )
    f.close()
    if gather:
        result.append( "\n" )   
    if not found:
        print( "example not found: %s %s" % ( file_name, marker ))
    return result
    
    
# ===========================================================================

def ref( 
    prefix,
    arg,
    name = None
):
    if arg[ 0 ] == "#":
        arg = arg[1:]
        if name is None:
            name = arg
        return f"{prefix}`{name} <#{arg}>`_\n"
        
    if name is not None:
        return f"{prefix}`{name} <{arg}>`_\n"
    
    else:
        return f"{prefix}:class:`~{arg}`\n"       
    
# ===========================================================================
#
# read file, handle
#    identification of the file into the result
#    $$document( yes / no )
#    $$methods()
#    $$image( <file>, 
#
# ===========================================================================

def read_source_file( file_name ):
    result = []
    use = True
    with open( file_name, "r" ) as file:
    
        result.append( f"\n\n#=> from {file_name}\n\n" )    
    
        for nr, line in enumerate( file.readlines() ):
            reporter = report( file_name, nr + 1, line )
            command, parameters = embedded_command( 
                reporter, 
                line, 
                [ 
                    "document", 
                    "methods", 
                    "insert_image", 
                    "add_table", 
                    "see_also",
                    "ref",
                    "insert_example"
                ] 
            )
            
            line = line.replace( "-gf.", "-g-f." ).replace( "gf.", "" ).replace( "-g-f.", "-gf." )
            line = line.replace( "godafoss.", "" )
            
            if command == "document":
                try:
                    use = bool( eval( parameters ) )
                except:
                    reporter.report( "invalid parameter" )
                    
            elif not use:
                pass
                
            elif command == "see_also":
                try:
                    prefix = line[ : line.find( "$$" ) ]
                    result.append( eval( f"see_also( '{prefix}', {parameters} )" ) )
                except Exception as error:
                    reporter.report( error )                            
                    
            elif command == "ref":
                try:
                    prefix = line[ : line.find( "$$" ) ]
                    result.append( eval( f"ref( '{prefix}', {parameters} )" ) )
                except Exception as error:
                    reporter.report( error )                            
                    
            elif command == "insert_example":
                try:
                    prefix = line[ : line.find( "$$" ) ]
                    for x in eval( f"insert_example( '{prefix}', {parameters} )" ):
                        result.append( x )
                except Exception as error:
                    reporter.report( error )                            
                    
            elif command == "insert_image":
                try:
                    prefix = line[ : line.find( "$$" ) ]
                    result.append( eval( f"insert_image( '{prefix}', {parameters} )" ) )
                except Exception as error:
                    reporter.report( error )
                    
            elif command == "add_table":
                s = f"add_table( {parameters} )"
                try:
                    exec( s )
                except Exception as error:
                    reporter.report( f"{error} in {s}" )
                
            elif command == "methods":    
                line_prefix = line.find( "$$methods" ) * " "
                result.append( line_prefix + '"""\n' )
                name = file_name.replace( ".py", "__" )
                item_prefix = os.path.basename( name )
                for f in glob.glob( name + "*.py" ):
                    for method_line in read_source_file( f ):
                        # method_line = method_line.replace( file_name, "" )
                        method_line = method_line.replace( item_prefix, "" )
                        result.append( line_prefix + method_line )              
                result.append( line_prefix + '"""\n' )
            
            elif line.strip() == "import godafoss as gf":
                pass
                
            else:
                line = line.replace( "$-$", "" )            
                result.append( line )       
                
    return result                       

# ===========================================================================
#
# processing on the full input
#
# ===========================================================================

def process_lines( lines ):
    result = []
    for line in lines:
    
        reporter = report( "", 0, line )
        command, parameters = embedded_command( 
            reporter, 
            line, 
            [ 
                "insert_table",  
            ] 
        )    

        if command == "insert_table":
            s = eval( f"insert_table( {parameters} )" )
            for line in s:
                result.append( line )
                
        else:
            result.append( line )     
        
    return result

# ===========================================================================

def set_version():
    file = "make/sphinx/conf.py"
    with open( file ) as f:
        lines = f.readlines()
    with open( file, "w" ) as f:
        for line in lines:
            if line.startswith( "version =" ):
                line = f"version = '{godafoss.version}'\n"
            f.write( line )

# ===========================================================================
#
# main
#
# ===========================================================================

def prepare_documentation():

    if not os.path.isfile( "make/sphinx/prepare_documentation.py" ):
        raise Exception( "must be run from the root" )  
        
    set_version()        
        
    try:
        shutil.rmtree( "tempdir" )
    except:
        pass
    try:
        os.makedirs( "tempdir/godafoss" )
    except:
        pass        
        
    lines = []    
    for file_name in sorted_source_files( "godafoss" ):
        lines += read_source_file( file_name )  

    lines = process_lines( lines )    
        
    with open( "tempdir/godafoss/__init__.py", "w" ) as file:
        for line in lines:
            #print( line )
            file.write( line )          

# ===========================================================================

prepare_documentation()

# ===========================================================================
