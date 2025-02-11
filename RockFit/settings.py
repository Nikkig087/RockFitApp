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
from django.contrib.messages import constants as messages

if os.path.isfile("env.py"):
    import env
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


SECRET_KEY = os.environ.get("SECRET_KEY")


DEBUG = False
ALLOWED_HOSTS = [
    "8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net",
    ".herokuapp.com",
    "8000-nikkig087-rockfitapp-vlfx33iw9of.ws-eu117.gitpod.io"
]
CSRF_TRUSTED_ORIGINS = [
    "https://8000-nikkig087-rockfitapp-fisk89uva99.ws.codeinstitute-ide.net",
    "https://*.codeanyapp.com",
    "https://*.herokuapp.com",
]


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

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_PORT = 2525
EMAIL_HOST_USER = "6ca26c09b06434"
EMAIL_HOST_PASSWORD = "728b24367df913"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Rockfit <no-reply@rockfit.com>"

ACCOUNT_PASSWORD_RESET_REDIRECT_URL = (
    "/accounts/password_reset_done/"
)
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = (
    "/accounts/password_change_done/"
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ADMIN_EMAIL = (
    "Nikki@Rockfit.com"
)

ROOT_URLCONF = "RockFit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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


MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

WSGI_APPLICATION = "RockFit.wsgi.application"

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL")
    )
}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

AUTH_PASSWORD_VALIDATORS = [
 {
  "NAME":
  "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
 {
  "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
 {
     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
 {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ACCOUNT_EMAIL_VERIFICATION = "none"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_URL = "accounts/login/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dvgozeo62",
    "API_KEY": "877696538918354",
    "API_SECRET": "83XoStnIJI0Ux0Snby6soXqGmaE",
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1
site_name = "Rockfit.com"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
