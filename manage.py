#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    MU_CONFIG = os.getenv('MU_CONFIG', 'PRODUCTION')
    if MU_CONFIG == 'STAGING':
        settings = 'staging'
    elif MU_CONFIG == 'PRODUCTION':
        settings = 'production'
    else:
        settings = 'development'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', settings.title())
    os.environ.setdefault('DJANGO_SECRET_KEY',
                          os.getenv('MU_SECRET_KEY', 'None'))

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
