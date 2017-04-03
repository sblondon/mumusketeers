import logging
import os

import colored
import netifaces

import web.settings


def _get_localhost():
    for interface in netifaces.interfaces():
        config = netifaces.ifaddresses(interface).values()
        for param in config:
            addr = param[0].get("addr")
            if addr.startswith("192.168"):
                return addr


web.settings.APP_DIR = os.getcwd() + '/'
web.settings.BIN_DIR = web.settings.APP_DIR
web.settings.PERSISTENT_DIR = web.settings.APP_DIR + 'local.persistent/'
web.settings.FILE_STORAGE_NAME = web.settings.PERSISTENT_DIR + 'Data.fs'
web.settings.BLOBS_DIR = web.settings.PERSISTENT_DIR + "blobs/"
web.settings.CLIENT_STORAGE = {
    "zeo": ("localhost", 8800),
    "blob_dir": web.settings.BLOBS_DIR,
    "shared_blob_dir": True,
}
web.settings.LOG_FILE = web.settings.PERSISTENT_DIR + '/logs/wsgi.log'
web.settings.LOG_LEVEL = logging.DEBUG
web.settings.PORT = 8000
web.settings.HOST = "http://{}:{}".format(_get_localhost(), web.settings.PORT)
web.settings.FILES_ROOT_DIR = web.settings.PERSISTENT_DIR + 'files/'
web.settings.STATISTICS_DIR = web.settings.PERSISTENT_DIR + 'statistics/'
web.settings.NOTIFY_ON_500 = False
web.settings.NOTIFY_AUTHOR = web.settings.APP_NAME + '-local'

if __name__ == '__main__':
    info = "\tThe web service is available at " + web.settings.HOST
    print(colored.stylize(info, colored.fg("green")))

