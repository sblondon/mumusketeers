import logging
import tempfile

APP_NAME = "mumusketeers"
COOKIE_NAME = APP_NAME + ".cookie"
HOST = "http://localhost:80"

APP_DIR = "."
PERSISTENT_DIR = tempfile.mkdtemp() + "/"
CLIENT_STORAGE = {"filename": PERSISTENT_DIR + "Data.fs"}
BLOBS_DIR = PERSISTENT_DIR + "blobs/"
FILES_ROOT_DIR = PERSISTENT_DIR + "files/"
STATISTICS_DIR = PERSISTENT_DIR + "statistics/"
LOGS_DIR = PERSISTENT_DIR + "logs/"
LOGS_CONFIG_FILE = PERSISTENT_DIR + "config.ini"
LOG_FILE = PERSISTENT_DIR + "logs/wsgi.log"
LOG_LEVEL = logging.DEBUG
SESSIONS_DIRECTORY = "/tmp/" + APP_NAME + "/sessions/"

DEBUG = True

NOTIFY_AUTHOR = APP_NAME
NOTIFY_LOG_ONLY = True
NOTIFY_ON_500 = False

TEMPLATES_DIRS=("web/templates/", "mailings/templates")

SMTP_SERVER = "localhost"

