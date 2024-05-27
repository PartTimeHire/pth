from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drops the django_admin_log table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS django_admin_log;')
        self.stdout.write(self.style.SUCCESS('Successfully dropped django_admin_log table'))
