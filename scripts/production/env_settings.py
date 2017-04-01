import web.settings

web.settings.HOST = "http://app.web.fr"
web.settings.APP_DIR = "/opt/app/production"
web.settings.PERSISTENT_DIR = web.settings.APP_DIR + ".persistent/"
web.settings.FILE_STORAGE_NAME = web.settings.PERSISTENT_DIR + "Data.fs"
web.settings.CLIENT_STORAGE = {"zeo": ("localhost", 8888)}
web.settings.FILES_ROOT_DIR = web.settings.PERSISTENT_DIR + "files/"
web.settings.STATISTICS_DIR = web.settings.PERSISTENT_DIR + "statistics/"
web.settings.LOG_FILE = web.settings.PERSISTENT_DIR + "logs/wsgi.log"
web.settings.DEBUG = False
web.settings.NOTIFY_LOG_ONLY = False
web.settings.NOTIFY_ON_500 = True

