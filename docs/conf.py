# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------


# -- Project information -----------------------------------------------------

project = "djlint"
copyright = "2021, Riverside Healthcare"
author = "Christopher Pickering"
release = "0.6.9"
version = release

# -- General configuration ---------------------------------------------------

extensions = ["myst_parser", "sphinx_copybutton", "sphinx_sitemap"]

templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "_assets",
    "node_modules",
    "gulpfile.js",
    "package.json",
    "package-lock.json",
    "requirements.txt",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_title = "djLint » "
html_favicon = "_static/favicon.ico"
language = "en"

html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
    ]
}

html_theme_options = {
    "show_related": False,
    "description": "Html Template Linter and Formatter",
    "github_button": True,
    "github_user": "Riverside-Healthcare",
    "github_repo": "djlint",
    "github_type": "star",
    "show_powered_by": False,
    "fixed_sidebar": True,
    "logo": "icon.png",
}

html_static_path = ["_static"]

source_suffix = [".rst", ".md"]

pygments_style = "sphinx"

html_css_files = [
    "css/style.css",
]

# -- Sitemap -------------------------------------------------------------------

html_baseurl = "https://djlint.com/"
html_extra_path = ["robots.txt"]
sitemap_url_scheme = "{link}"
