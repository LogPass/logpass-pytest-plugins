"""Minimal and test-efficient Django's settings."""

SECRET_KEY = 'not very secret in tests'
INSTALLED_APPS = ('rest_framework', 'channels')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# channels
ASGI_APPLICATION = 'asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
