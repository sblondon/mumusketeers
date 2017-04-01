import web.settings

web.settings.HOST = "http://recette.app.yaal.fr"
web.settings.APP_DIR = "/opt/app/recette"
web.settings.PERSISTENT_DIR = web.settings.APP_DIR + ".persistent/"
web.settings.FILE_STORAGE_NAME = web.settings.PERSISTENT_DIR + "Data.fs"
web.settings.CLIENT_STORAGE = {"zeo": ("localhost", 8887)}
web.settings.FILES_ROOT_DIR = web.settings.PERSISTENT_DIR + "files/"
web.settings.STATISTICS_DIR = web.settings.PERSISTENT_DIR + "statistics/"
web.settings.LOG_FILE = web.settings.PERSISTENT_DIR + "logs/wsgi.log"
web.settings.NOTIFY_AUTHOR = web.settings.APP_NAME + "-recette"

