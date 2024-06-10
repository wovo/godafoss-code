# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath( '../../tempdir' ) )
sys.path.insert(0, os.path.abspath( 'mocks' ) )


# -- Project information -----------------------------------------------------

project = 'godafoss'
version = '0.2'
release = version
copyright = '2024, Wouter van Ooijen'
author = 'Wouter van Ooijen'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
   'sphinx.ext.autodoc', 
   'sphinx.ext.coverage', 
   'sphinx.ext.napoleon',
   'rst2pdf.pdfbuilder', 
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'  
html_theme_options = {
    "collapsiblesidebar" : "true",
}
#add_module_names = False

html_sidebars = {
#   '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
   '**': ['searchbox.html'],
#   'using/windows': ['windowssidebar.html', 'searchbox.html'],
}
html_show_copyright = True

html_logo = "logo.png"
html_favicon = "flavicon.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

nitpick_ignore = [('py:class', 'object' )]

pdf_documents = [( 'index', project, project, author ),]

# from https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method

def skip( app, what, name, obj, would_skip, options):
#    if would_skip:
#        pass
#        #print( name )
    if name in [ 
        "__repr__", "_str__", "__init__",
    ]:
        return obj.__doc__ != ""
        
    if name in [
        "MethodType", "SPI", "I2C", 
    ]:
        return True
        
    return would_skip

def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.add_css_file('my_theme.css')    
    
# https://stackoverflow.com/questions/25145817/ellipsis-truncation-on-module-attribute-value-in-sphinx-generated-documentatio/25163963#25163963    

from sphinx.ext.autodoc import DataDocumenter, ModuleLevelDocumenter, SUPPRESS
#from sphinx.util.inspect import safe_repr

def add_directive_header(self, sig):
    ModuleLevelDocumenter.add_directive_header(self, sig)
    if not self.options.annotation:
            # PATCH: 
            objrepr = "..." 
    elif self.options.annotation is SUPPRESS:
        pass
    else:
        self.add_line(u'   :annotation: %s' % self.options.annotation,
                      '<autodoc>')

DataDocumenter.add_directive_header = add_directive_header   

add_module_names = False 

#html_theme = 'sphinx_rtd_theme'
#html_style = 'css/my_theme.css'
