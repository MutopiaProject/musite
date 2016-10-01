from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

"""Command to create a default admin account
"""
class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin',
                                          password='admin',
                                          email='')
