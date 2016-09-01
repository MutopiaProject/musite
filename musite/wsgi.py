import os

from configurations.wsgi import get_wsgi_application

MU_CONFIG = os.getenv('MU_CONFIG', 'PRODUCTION')
if MU_CONFIG == 'STAGING':
    settings = 'staging'
elif MU_CONFIG == 'DEVELOPMENT':
    settings = 'development'
else:
    settings = 'production'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musite.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', settings.title())
os.environ.setdefault('DJANGO_SECRET_KEY',
                      os.getenv('MU_SECRET_KEY', 'None'))

application = get_wsgi_application()
