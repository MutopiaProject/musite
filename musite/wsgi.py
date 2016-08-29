import os

from configurations.wsgi import get_wsgi_application

MU_CONFIG = os.getenv('MU_CONFIG', 'PRODUCTION')
if MU_CONFIG == 'STAGING':
    settings = 'staging'
elif MU_CONFIG == 'PRODUCTION':
    settings = 'production'
else:
    settings = 'development'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musite.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

application = get_wsgi_application()
