from django.apps import AppConfig

class FitnessConfig(AppConfig):
    """
    Configuration class for the 'fitness' Django application.

    This class defines the default behavior and configuration for the app,
    including the default auto field and any initialization logic.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness'

    def ready(self):
        """
        Initialization logic for the 'fitness' app.

        This method is called when the application is ready. It imports
        the 'signals' module to ensure that signal handlers are connected
        and ready to handle events such as model changes.
        """
        import fitness.signals  # Ensure this import is inside the method
