import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# --- BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# load .env from project root (only in development / if present)
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

# --- SECURITY / BASE SETTINGS ---
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    # если DEBUG=True — допускаем временный ключ,
    # в продакшене обязательно задайте SECRET_KEY
    if os.getenv("DEBUG", "True").lower() in ("1", "true", "yes"):
        SECRET_KEY = "dev-secret-key"
    else:
        raise RuntimeError(
            "SECRET_KEY is not set in environment for production!")

DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS через env, разделённые запятой
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# --- INSTALLED APPS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "info",
]

# S3 / Object Storage support (Yandex/Object Storage)
USE_S3 = os.getenv("USE_S3", "False").lower() in ("1", "true", "yes")
if USE_S3:
    INSTALLED_APPS += ["storages"]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # serve static files in production without external server
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "voenkom.urls"

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "voenkom.wsgi.application"

# --- DATABASE ---
DATABASE_URL = os.getenv("DATABASE_URL") or None
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", 600)),
            ssl_require=os.getenv("DB_SSL_REQUIRE", "False").lower() in (
                "1", "true", "yes") and not DEBUG,
        )
    }
else:
    # default: sqlite (good for simple deploy / testing).
    # For production consider managed postgres.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Internationalization ---
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles"))

# WhiteNoise for simple static handling in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if USE_S3:
    # store media files in S3 (Yandex Object Storage)
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # e.g. https://storage.yandexcloud.net
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "")
    AWS_S3_SIGNATURE_VERSION = os.getenv("AWS_S3_SIGNATURE_VERSION", "s3v4")
    # MEDIA_URL можно указывать как полный путь, если требуется CDN
    MEDIA_URL = os.getenv(
        "MEDIA_URL", f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/")
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))

# --- Email ---
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv(
    "EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "voenkom.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_FILE),
            "maxBytes": 1_000_000,
            "backupCount": 3,
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        }
    },
    "root": {
        "handlers": ["file", "console"],
        "level": LOG_LEVEL,
    },
}

# --- Security for production ---
# Build CSRF_TRUSTED_ORIGINS automatically from ALLOWED_HOSTS (only https)
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    host = host.strip()
    if not host:
        continue
    # if host already includes schema use it, else assume https
    if host.startswith("http://") or host.startswith("https://"):
        CSRF_TRUSTED_ORIGINS.append(host)
    else:
        CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in (
    "1", "true", "yes") and not DEBUG

# Clickjacking / HSTS
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = int(
    os.getenv("SECURE_HSTS_SECONDS", 0)) if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower() in ("1", "true", "yes")
SECURE_HSTS_PRELOAD = os.getenv(
    "SECURE_HSTS_PRELOAD", "False").lower() in ("1", "true", "yes")

# --- Default primary key ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
