import os

ALLOWED_HOSTS = ["*"]

DATABASES = {
  "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "db-8300", "USER": "postgres", "HOST": "postgres"}
}

DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

INSTALLED_APPS = [
  "rest_framework",
  "jboard",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [],
  "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
  "DEFAULT_SCHEMA_CLASS": "jboard.schema.Schema",
  "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
  "UNAUTHENTICATED_USER": None,
}

ROOT_URLCONF = "jboard.urls"

SECRET_KEY = "SECRET-KEY"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

WSGI_APPLICATION = "jboard.wsgi.application"

GITHUB_JOBS_CONSUMER_BASE_URL = "https://jobs.github.com/"
