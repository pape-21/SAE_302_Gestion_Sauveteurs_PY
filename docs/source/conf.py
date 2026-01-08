# Configuration file for the Sphinx documentation builder.
import os
import sys

# --- MODIFICATION MAJEURE ICI ---
# On dit à Sphinx : "Remonte de 2 dossiers pour trouver le code source"
# Si conf.py est dans docs/source/, ../.. nous amène à la racine du projet.
sys.path.insert(0, os.path.abspath('../..'))
# --------------------------------

# -- Project information -----------------------------------------------------
project = 'Application graphique de gestion des sauveteurs spéléologues'
copyright = '2025, Pape Birame Fall, Mohamed Fall, Perceval Behanzin, Sokhna Gueye'
author = 'Pape Birame Fall, Mohamed Fall, Perceval Behanzin, Sokhna Gueye'
release = '0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.autodoc',   # Lit le code
    'sphinx.ext.viewcode',  # Ajoute des liens vers le code source
    'sphinx.ext.napoleon'   # <--- INDISPENSABLE : Pour le style Google (Args/Returns)
]

# Configuration de Napoleon (pour que ça soit joli)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']