import os

import logging
import logging.config
import logging.handlers

import ysessions
import ystatistics
import ytemplates
import ywsgi
import yzodb

import web.settings
import web.public.app
import web.admin.app
import web.players.app
import web.filters
import web.middlewares


application = None


class YApp(object):

    def __init__(self):
        self._apps = (
                web.public.app.get(),
                web.admin.app.get(),
                web.players.app.get(),
            )

    def __call__(self, request):
        with yzodb.connection():
            for _app in self._apps:
                _response = _app(request)
                if _response:
                    return _response
            return web.public.views.not_found(request)


def make():
    try:
        os.mkdir(web.settings.LOGS_DIR)
    except OSError:
        pass
    try:
        logging.config.fileConfig(web.settings.LOGS_CONFIG_FILE,
                defaults={
                    "logs_dir": web.settings.LOGS_DIR,
                    })
    except KeyError:
        logging.basicConfig(filename=web.settings.LOGS_DIR + "tests.log")

    ytemplates.init(templates_dirs=web.settings.TEMPLATES_DIRS)
    ytemplates.get_env_jinja().filters['level_to_bootstrap_class'] = web.filters.level_to_bootstrap_class
    ytemplates.get_env_jinja().filters['pretty_boolean'] = web.filters.pretty_boolean
    ytemplates.get_env_jinja().filters['shuffle'] = web.filters.shuffle
    ystatistics.init(web.settings.STATISTICS_DIR)
    if not yzodb.connection_pool():
        yzodb.make_connection_pool(**web.settings.CLIENT_STORAGE)
        yzodb.set_files_root_dir(web.settings.FILES_ROOT_DIR)

    _app = YApp()
    _app = ysessions.SessionsMiddleware(_app, cookie_name=web.settings.COOKIE_NAME, sessions_directory=web.settings.SESSIONS_DIRECTORY)
    _app = ystatistics.WriteCycleTimeMiddleware(_app)
    _app = web.middlewares.ExceptionsMiddleware(_app, web.settings.DEBUG)

    return ywsgi.make(_app)

