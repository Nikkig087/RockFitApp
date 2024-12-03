"""
Configuration module for the 'fitness' application.

This module configures the AppConfig class for the fitness app, including 
custom initialization logic such as importing signal handlers.
"""
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
        import fitness.signals  # to import the signals module
        """
        Initialization logic for the 'fitness' app.

        This method is called when the application is ready. It imports
        the 'signals' module to ensure that signal handlers are connected
        and ready to handle events such as model changes.
        """


class FitnessConfig(AppConfig):
     """
    Alternative configuration class for the 'fitness' app.

    This version of the class does not set a default auto field but still
    includes initialization logic to import signal handlers.
    """
    name = 'fitness'

    def ready(self):
     """
        Initializes the 'fitness' app by importing the signals module.

        This ensures that signal handlers defined in the 'fitness.signals'
        module are registered and will be triggered by relevant events.
        """
        import fitness.signals
