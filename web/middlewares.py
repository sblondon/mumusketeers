import logging
import werkzeug
import ywsgi
import yzodb

import web.public.app
import web.settings


class ExceptionsMiddleware(object):
    def __init__(self, app, debug):
        self._app = app
        self._debug = debug

    def __call__(self, request):
        try:
            return  self._app(request)
        except yzodb.ObjectNotFoundException as ex:
            logging.warning('Exception "{exc}" on URL {url}'.format(exc=str(ex), url=request.path))
            if self._debug:
                _report = ywsgi.format_exc(request)
                _report += "\nErreur attrapee par ExceptionsMiddleware\n"
                return ywsgi.text(_report, status=404)
            return web.public.views.object_not_found(request)
        except werkzeug.exceptions.BadRequest as ex:
            if self._debug:
                _report = ywsgi.format_exc(request)
                _report += "\nErreur attrapee par ExceptionsMiddleware\n"
                return ywsgi.text(_report, status=403)
            return web.public.views.bad_request(request)
        except Exception as ex:
            _report = ywsgi.format_exc(request)
            _report += "\nErreur attrapee par ExceptionsMiddleware\n"
            logging.error(_report)
            if self._debug:
                return ywsgi.text(_report, status=500)
            else:
                return web.public.views.error(request)
