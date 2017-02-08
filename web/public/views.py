import ywsgi

import web.public.pages


def not_found(request):
    _page = web.public.pages.NotFound()
    return ywsgi.html(_page.render(), status=404)


def home(request):
    _page = web.public.pages.Home()
    return ywsgi.html(_page.render())


def bad_request(request):
    _page = web.public.pages.BadRequest()
    return ywsgi.html(_page.render(), status=400)


def object_not_found(request):
    _page = web.public.pages.ObjectNotFound()
    return ywsgi.html(_page.render(), status=404)


def error(request):
    _page = web.public.pages.InternalServerError()
    return ywsgi.html(_page.render(), status=500)

