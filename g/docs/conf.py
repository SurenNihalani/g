"""Sphinx configuration."""
project = "g"
author = "Suren Nihalani"
copyright = "2022, Suren Nihalani"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
