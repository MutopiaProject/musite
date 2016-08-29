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

version = '1.0'
release = '1.0.1'

language = None

exclude_patterns = ['_build',]

pygments_style = 'sphinx'
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'

html_theme_options = {
    'logo': 'mutopia-logo.svg',
    'logo_name': False,
    'fixed_sidebar': True,
}

#html_logo = 'graphics/mutopia-logo.svg'
html_favicon = 'graphics/favicon.ico'

html_static_path = ['_static', 'graphics', ]

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

#mupub_path = os.path.abspath('../../mupub/docs/_build/html')
mupub_path = 'http://mutopia-rewrite.readthedocs.io/en/latest/'
intersphinx_mapping = { 'python': ('https://docs.python.org/3', None),
                        'mupub': (mupub_path, None), }
