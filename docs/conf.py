import os
import sys
import django
from datetime import datetime
import configurations

sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musite.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
os.environ.setdefault('DJANGO_SECRET_KEY',
                      os.getenv('MU_SECRET_KEY', 'None'))
configurations.setup()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'configurations.sphinx',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# General information about the project.
project = 'Mutopia Devo'
year = datetime.now().year
copyright = u'%d, The Mutopia Project' % year
author = 'Glen Larsen'

version = '1.1'
release = '1.1.0'

language = None

exclude_patterns = ['_build',]

pygments_style = 'sphinx'
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static', 'graphics', ]

mupub_path = 'http://mutopia-rewrite.readthedocs.io/en/latest/'
intersphinx_mapping = { 'python': ('https://docs.python.org/3', None),
                        'mupub': (mupub_path, None), }
