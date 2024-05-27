from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Fixes the inconsistent migration history'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Insert the missing authentication migration
            cursor.execute(
                """
                INSERT INTO django_migrations (app, name, applied) 
                SELECT 'authentication', '0001_initial', CURRENT_TIMESTAMP 
                WHERE NOT EXISTS (
                    SELECT 1 FROM django_migrations WHERE app='authentication' AND name='0001_initial'
                )
                """
            )
            # Delete all admin migrations
            cursor.execute(
                """
                DELETE FROM django_migrations WHERE app='admin'
                """
            )
            # Reinsert admin migrations in the correct order
            cursor.execute(
                """
                INSERT INTO django_migrations (app, name, applied) VALUES 
                ('admin', '0001_initial', CURRENT_TIMESTAMP),
                ('admin', '0002_logentry_remove_auto_add', CURRENT_TIMESTAMP),
                ('admin', '0003_logentry_add_action_flag_choices', CURRENT_TIMESTAMP)
                """
            )
            transaction.commit()
        self.stdout.write(self.style.SUCCESS('Successfully fixed the migration history'))
