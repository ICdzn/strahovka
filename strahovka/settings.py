"""
This is an optional file that defined app level settings such as:
- database settings
- session settings
- i18n settings
This file is provided as an example:
"""
import os

# db settings
APP_FOLDER = os.path.dirname(__file__)
APP_NAME = os.path.split(APP_FOLDER)[-1]
# DB_FOLDER:    Sets the place where migration files will be created
#               and is the store location for SQLite databases
DB_FOLDER = os.path.join(APP_FOLDER, "databases")
DB_URI = 'sqlite://models_change10.db'
DB_POOL_SIZE = 1

# send email on regstration
VERIFY_EMAIL = True
# account requires to be approved ?
REQUIRES_APPROVAL = False
# email settings
SMTP_SERVER = 'smtp.gmail.com:587'
SMTP_SENDER = "strahovka.work2020@gmail.com"
SMTP_LOGIN = "strahovka.work2020@gmail.com:cdnblpUYBvdlH8"
SMTP_TLS = True

# session settings
SESSION_TYPE = "cookies"
SESSION_SECRET_KEY = "<my secret key>"
MEMCACHE_CLIENTS = ["127.0.0.1:11211"]
REDIS_SERVER = "localhost:6379"

# logger settings
LOGGERS = [
    "warning:stdout"
]  # syntax "severity:filename" filename can be stderr or stdout

# single sign on Google (will be used if provided)
OAUTH2GOOGLE_CLIENT_ID = None
OAUTH2GOOGLE_CLIENT_SECRET = None

# single sign on Google (will be used if provided)
OAUTH2FACEBOOK_CLIENT_ID = None
OAUTH2FACEBOOK_CLIENT_SECRET = None

# enable PAM
USE_PAM = False

# enable LDAP
USE_LDAP = False
LDAP_SETTING = {
    "mode": "ad",
    "server": "my.domain.controller",
    "base_dn": "ou=Users,dc=domain,dc=com",
}

# i18n settings
T_FOLDER = os.path.join(APP_FOLDER, "translations")

# Celery settings
USE_CELERY = False
CELERY_BROKER = 'redis://localhost:6379/0'

# try import private settings
try:
    from .settings_private import *
except:
    pass
