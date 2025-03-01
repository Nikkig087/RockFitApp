from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# Debug
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allowed hosts
ALLOWED_HOSTS = [
    "8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net",
    ".herokuapp.com",
    "8000-nikkig087-rockfitapp-vlfx33iw9of.ws-eu117.gitpod.io",
    '8080-nikkig087-rockfitapp-vlfx33iw9of.ws-eu117.gitpod.io',
    '8000-nikkig087-rockfitapp-vlfx33iw9of.ws-eu118.gitpod.io',
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net",
    "https://*.codeanyapp.com",
    "https://*.herokuapp.com",
]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
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
    "fitness",
    "RockFit",
    "cart",
    "csp",
    "imagekit",
    "whitenoise.runserver_nostatic",
]

# Middleware
MIDDLEWARE = [
    "django_brotli.middleware.BrotliMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "RockFit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "fitness.context_processors.cart_count",
                "fitness.context_processors.wishlist_count",
            ],
        },
    },
]

WSGI_APPLICATION = "RockFit.wsgi.application"

# Database configuration
DATABASES = {
    "default": dj_database_url.parse(os.getenv("DATABASE_URL"))
}


# Stripe configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

# Ensure proper Anymail configuration
SENDINBLUE_API_KEY = os.getenv("SENDINBLUE_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

ANYMAIL = {
    "SENDINBLUE": {
        "API_KEY": SENDINBLUE_API_KEY,
    }
}

EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}



# Storage settings
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Additional configurations
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10
