from .settings import *


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
STATIC_URL = '/static/'
STORAGES = {
    'default': {
        'BACKEND': "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    'staticfiles': {
        'BACKEND': "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
