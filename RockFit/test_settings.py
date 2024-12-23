from .settings import *

# Use an in-memory SQLite database for testing (so it doesn't touch your production DB)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',  # In-memory database for tests
}

# Disable sending real emails during tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Set the media root and static root to temporary directories during tests
STATIC_URL = '/static/'

STORAGES = {
    'default': {
        'BACKEND': "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    'staticfiles': {
        'BACKEND': "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}



# Additional test-specific settings can go here (for example, cache settings, etc.)
