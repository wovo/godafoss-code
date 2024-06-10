# ===========================================================================
#
# file     : test.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license attribute (from license.py)
#
# ===========================================================================

import godafoss as gf
try:
    import glob
    import os
    import shutil
except:
    pass

# ===========================================================================

# command line and coverage are only supported when running native,
# not for running on MicroPython
try:
    import coverage
    check_coverage = True
    import sys
    unit_to_test = None if len( sys.argv ) == 1 else sys.argv[ 1 ]
except:
    check_coverage = False
    unit_to_test = None


# ===========================================================================

def run_tests( name: str = None ):
    if name is not None:
        eval( f"gf.unit_test_{name}()" )
        return

    gf.unit_test_basics()
    gf.unit_test_one()
    gf.unit_test_bits()
    gf.unit_test_bytes()
    gf.unit_test_repeater()
    gf.unit_test_immutable()
    gf.unit_test_no_new_attributes()
    gf.unit_test_fraction()
    gf.unit_test_temperature()
    gf.unit_test_xy()
    gf.unit_test_xyz()
    gf.unit_test_color()
    gf.unit_test_pins()
    gf.unit_test_ports()
    gf.unit_test_terminal()
    gf.unit_test_canvas()


# ===========================================================================

def complain( path, file, number, line, message ):
    line = line.rstrip()
    print( f"[{path}] {file}:{number} {message}" )
    print( f"    [{line}]" )

# ===========================================================================

def fixed_lines( file ):
    return [
        "# " + 75 * "=",
        "#",
        f"# file     : {file}",
        "# part of  : godafoss micropython library",
        "# url      : https://www.github.com/wovo/godafoss",
        "# author   : Wouter van Ooijen (wouter@voti.nl) 2024",
        "# license  : MIT license, see license attribute (from license.py)",
        "#",
        "# " + 75 * "=",
    ]

# ===========================================================================

def check_one_source_file( path, file ):

    # some files by necessity contain long lines
    check_long_lines = path.find( "docs" ) == -1

    # some files can't be loaded because they reply on MicroPython
    # -specific features
    for exclude in (
        "boards",
        "chips",
#        "demos"
    ):
        if path.find( exclude ) > -1:
           return

    # some files can't be loaded because they reply on MicroPython
    # -specific features
    if file in (
        "spi.py",
        "target_rp2040.py",
        "__init__mpy.py"
    ):
        return

    if 0:
        print( "checke source file", path, file )

    component = file.replace( ".py", "" )

    # first check: importing must succeed
    eval( f"gf.{component}" )

    with open( f"{path}/{file}" ) as source:
        lines = source.readlines()

    fixed = fixed_lines( file )
    if file == "license.py":
        fixed[ 6 ] = \
            "# license  : MIT license, see license variable in this file"

    modified = False
    for number, line in enumerate( lines ):

        strip_line = line.replace( "\n", "" )
        if ( number < 9 ) and ( strip_line != fixed[ number ] ):
            complain( path, file, number + 1, line, "header not correct" )

        old = line
        line = old.rstrip() + "\n"
        if old != line:
            #print( f"[{old}]\n[{line}]" )
            complain( path, file, number + 1, line, "line stripped" )
            lines[ number ] = line
            modified = True

        p = line.find( "#" + " =====" )
        if p > -1:
            if p not in [ -1, 0, 4, 8 ]:
                complain( path, file, number + 1, line, "start # ===" )
            if len( line ) != 78:
                complain( path, file, number + 1, line, "end # ===" )

        if check_long_lines and len( line ) > 78:
            complain( path, file, number + 1, line, "line too long" )

    if modified:
        with open( path + "/" + file, "w" ) as source:
            for line in lines:
                source.write( line )

# ===========================================================================

def check_all_source_files( path ):
    for entry in os.listdir( path ):
        if entry.endswith( ".py" ):
            check_one_source_file( path, entry )
        elif entry.find( "." ) < 0:
            check_all_source_files( path + "/" + entry )

# ===========================================================================

def test():

    if check_coverage:
        cov = coverage.Coverage(
            branch = True,
            #check_preimported = True,
            omit = [
            #    "godafoss\\__init__.py",
            #    "godafoss\\tests\\*",
            ]
        )
        cov.start()

    if unit_to_test is not None:
        run_tests( unit_to_test )
    else:
        if not gf.running_micropython:
            check_all_source_files( "godafoss" )
        run_tests()
        print( "all tests done" )

    if ( not gf.running_micropython ) and check_coverage:
       cov.stop()
       cov.report( show_missing = True )

    if not gf.running_micropython:
        for entry in glob.glob(
            "godafoss/**/__pycache__",
            recursive = True
        ):
            shutil.rmtree( entry )


# ===========================================================================

