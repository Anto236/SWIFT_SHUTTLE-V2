from django.apps import AppConfig
from django.core.management import call_command

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Run command after app loads (won't affect migrations)
        try:
            call_command('create_admin_user', verbosity=0)
        except Exception as e:
            pass  # Ignore errors during migration phase
