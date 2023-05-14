# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Timecode'
copyright = '2023, Michael J. Jordan'
author = 'Michael J. Jordan'

release = '0.1'
version = '0.1.0'

# -- General configuration

autodoc_member_order = 'bysource'

extensions = [
	'sphinxcontrib.jquery',
	'sphinx.ext.duration',
	'sphinx.ext.doctest',
	'sphinx.ext.autodoc',
	'sphinx.ext.autosummary',
	'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
	'python': ('https://docs.python.org/3/', None),
	'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
	'collapse_navigation': False,
	'style_external_links': False,
}

# -- Options for EPUB output
epub_show_urls = 'footnote'