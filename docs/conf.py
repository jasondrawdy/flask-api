# #########################################################################
# Description:
# Configuration file for the Sphinx documentation builder.
# #########################################################################
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
project = 'My Project'
copyright = '2023, Jason Drawdy'
author = 'Jason Drawdy'

# The full version, including alpha/beta/rc tags
release = '1.0'

# -- General configuration ---------------------------------------------------
autoapi_dirs = ['..']
autodoc_typehints = 'description'
autoapi_ignore = ['*/tests.py*', '*/setup.py*', '*/plugins*', '*/docs*']
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
	'autoapi.extension'
]
add_module_names = False
napoleon_google_docstring = False
napoleon_numpy_docstring = True
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None)
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
cmd_line_template = "sphinx-apidoc --module-first -f -o {outputdir} {moduledir}"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_short_title = f'{project} {release} Documentation'
html_static_path = ['_static']
html_show_sourcelink = False
html_show_sphinx = False