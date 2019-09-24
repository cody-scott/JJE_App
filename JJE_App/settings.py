import os
import sys
import dj_database_url


def _check_os_condition(condition, target):
    if os.environ.get(condition, "") == target:
        return True
    else:
        return False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "EMPTYSECRET")

DEBUG = False
ACCOUNT_EMAIL_VERIFICATION = "optional"
ALLOWED_HOSTS = ['jje-league.herokuapp.com', 'jje-test-site.herokuapp.com']
if os.environ.get("DEBUG", "") == "True":
    DEBUG = True
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    ACCOUNT_EMAIL_VERIFICATION = "none"
    ALLOWED_HOSTS += ['127.0.0.1', '0.0.0.0', 'localhost', 'www.myapp.new', "*"]

INTERNAL_IPS = ["127.0.0.1"]
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

INSTALLED_APPS = [
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'debug_toolbar',

    'rest_framework',

    'JJE_Waivers.apps.JJEWaiversConfig',
    'JJE_Standings.apps.JJEStandingsConfig',
    'JJE_oauth.apps.JJEOauthConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',


]

ROOT_URLCONF = 'JJE_App.urls'

LOGIN_REDIRECT_URL = 'index'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'JJE_App.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {},
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'est.tdb'),
            'TEST_NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
        }
    }
    ACCOUNT_EMAIL_VERIFICATION = "none"
elif not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "sharedstatic"),
]

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'

try:
    from JJE_App.private_config import \
        email_user, email_password, client_id, client_secret, database_url

    EMAIL_HOST_USER = email_user
    EMAIL_HOST_PASSWORD = email_password
    ADMINS = (('Admin', email_user),)
    client_id = client_id
    client_secret = client_secret

    db_from_env = dj_database_url.parse(database_url, conn_max_age=500)
    DATABASES['default'].update(db_from_env)

except:
    EMAIL_HOST_USER = os.environ.get("email_user")
    EMAIL_HOST_PASSWORD = os.environ.get("email_password")
    ADMINS = (('Admin', os.environ.get("email_user")),)
    # These are for the api
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_sec")

EMAIL_PORT = 587

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

email_super_users = False
if _check_os_condition("SU_Email", "True"):
    email_super_users = True

email_admins = False
if _check_os_condition("AD_Email", "True"):
    email_admins = True

send_emails = True
if _check_os_condition("Send_Email", "False"):
    send_emails = False


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                ),
    'PAGE_SIZE': 50
}

LEAGUE_ID = os.environ.get("league_id")

DEBUG_TOOLBAR_CONFIG = {
  'JQUERY_URL':'',
}
