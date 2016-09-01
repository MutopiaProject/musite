"""
Django settings for musite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from configurations import Configuration, values

class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'mutopia',
        'update',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'musite.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'musite.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mutodb',
            'USER': 'muuser',
            'PASSWORD': 'mumusic',
            'HOST': 'localhost',
            'PORT': '5433',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VAIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/1.10/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


class Development(Common):
    """
    In-development settings and default configuration
    """
    DEBUG = values.BooleanValue(True)
    ALLOWED_HOSTS = ['127.0.0.0',]

    # Use "DEBUG" level to get DB query times (as well as expected
    # exceptions that are caught and ignored in the template system.)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            },
            'mutopia': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            },
            'update': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            },
        },
    }


class Production(Common):
    """
    In-production settings

    """

    if 'RDS_HOSTNAME' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
        }

    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(Common.BASE_DIR, '..', 'www', 'staticfiles')

    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )
