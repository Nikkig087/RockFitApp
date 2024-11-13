from django.apps import AppConfig


class FitnessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness'

    def ready(self):
        import fitness.signals  # to import the signals module


class FitnessConfig(AppConfig):
    name = 'fitness'

    def ready(self):
        import fitness.signals
