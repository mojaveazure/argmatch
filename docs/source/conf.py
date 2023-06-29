# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# import sphinx_bootstrap_theme

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'argmatch'
copyright = '2023, Paul Hoffman'
author = 'Paul Hoffman'

# -- Options for Napoleon ----------------------------------------------------

napoleon_google_docstring = True
napoleon_include_private_with_doc = False

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
# html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
# html_theme_options = {
#     'bootswatch_theme': 'flatly',
#     'bootstrap_version': '3'
# }

html_static_path = ['_static']
