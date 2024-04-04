# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MatFeaLib'
copyright = '2024, MatFeaLib Developers'
author = 'MatFeaLib Developers'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx_rtd_theme',
        'sphinx-prompt'
        ]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    #'canonical_url': '',
 #   "logo_only": True,
 #   "display_version": True,
 #   "prev_next_buttons_location": "bottom",
 #   "style_external_links": False,
 #   "style_nav_header_background": "#343131",
    "style_nav_header_background": "#C0C0C0",
    # Toc options
 #   "collapse_navigation": True,
 #   "sticky_navigation": True,
 #   "navigation_depth": 4,
 #   "includehidden": True,
 #   "titles_only": False,
}
# html_favicon = "MatFeaLib-favicon.ico"
html_logo = './_static/MatFeaLib-logo-0323.png'

