import ywsgi

import web.public.pages


def not_found(request):
    page = web.public.pages.NotFound()
    return ywsgi.html(page.render(), status=404)


def home(request):
    page = web.public.pages.Home()
    return ywsgi.html(page.render())


def bad_request(request):
    page = web.public.pages.BadRequest()
    return ywsgi.html(page.render(), status=400)


def object_not_found(request):
    page = web.public.pages.ObjectNotFound()
    return ywsgi.html(page.render(), status=404)


def error(request):
    page = web.public.pages.InternalServerError()
    return ywsgi.html(page.render(), status=500)

