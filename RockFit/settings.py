"""
Django settings for RockFit project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
import os
import dj_database_url

if os.path.isfile("env.py"):
    import env


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure"
#"-+p1u592@#(4hl_3we%cick#(duz**l9sw2qz9$*_sthoa_!d#b"
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net','.herokuapp.com',]
CSRF_TRUSTED_ORIGINS = [
    "https://8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net",
    "https://*.codeanyapp.com",
    "https://*.herokuapp.com",


]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_summernote",
    "cloudinary",
    "cloudinary_storage",
    "compressor",
    'fitness',
    'RockFit',
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



ACCOUNT_PASSWORD_RESET_REDIRECT_URL = '/accounts/password_reset_done/'
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = '/accounts/password_change_done/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# settings.py
# settings.py

ADMIN_EMAIL = 'test@example.com'  # Dummy admin email for testing



ROOT_URLCONF = 'RockFit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'fitness.context_processors.cart_count',
                'fitness.context_processors.wishlist_count',
            ],
        },
    },
]

# Message tags to integrate with Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

WSGI_APPLICATION = 'RockFit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ACCOUNT_EMAIL_VERIFICATION = 'none'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_URL = 'accounts/login/'  # Default path for login if authentication fails
LOGIN_REDIRECT_URL = '/'  # Home page or your desired page
ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Redirect after signup
LOGOUT_REDIRECT_URL = '/'  # Redirect path after successful logout



STATICFILES_STORAGE = 'compressor.storage.CompressorFileStorage'
COMPRESS_ENABLED = True  # Enable compression
COMPRESS_URL = '/static/'  
COMPRESS_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

COMPRESS_OFFLINE = True  #  pre-compress files
COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'sass {infile} {outfile}'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # Add this line
]

DEFAULT_FILE_STORAGE = (
    "cloudinary_storage.storage.MediaCloudinaryStorage"
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dvgozeo62",
    "API_KEY": "877696538918354",
    "API_SECRET": "83XoStnIJI0Ux0Snby6soXqGmaE",
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10