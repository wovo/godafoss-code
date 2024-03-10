Scripts for creating

- the html documentation
- the pdf documentation
- the json distribution file
- pushing and pulling the github repository
- creating and viewing ggf files

These scripts are intended to be run from the root, for instance as

make/html

The documentation text is in docstrings in the Python source files.
These files are processed by the make_documentation.py script, 
which has a list of files to processes into the single 
tempdir/godafoss/__init__.py file.
While processing, it handles images and inline code examples.
The code examples are taken from the test/native test scripts.
The images are taken from the wovo/images repository, which must be
present alongside the godafoss repostitory.
