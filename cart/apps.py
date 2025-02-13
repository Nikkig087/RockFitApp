"""
App configuration for the cart application.

This module defines the configuration for the 'cart' app,
which is part of the Django project.
It specifies metadata and default settings related to the app.
"""

from django.apps import AppConfig

class CartConfig(AppConfig):
    """
    Configuration class for the cart application.

    This class provides metadata and settings for the 'cart' app, including the
    default primary key field type and the app's name.

    Attributes:
        default_auto_field (str):
        Specifies the default field type for primary keys.
        In this case, it uses 'django.db.models.BigAutoField'
        for auto-incrementing primary keys with large integers.
        name (str): The name of the app. This should match
        the app directory name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"


    def ready(self):
        import cart.signals  # Ensure signals are imported