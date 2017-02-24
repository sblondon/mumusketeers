import web.pages


class Home(web.pages.Page):
    url = '/'
    url_regex = '^{0}$'.format(url)
    template = 'public/index.html'


class NotFound(web.pages.Page):
    template = 'public/404.html'


class BadRequest(web.pages.Page):
    template = 'public/400.html'


class ObjectNotFound(web.pages.Page):
    template = 'public/object_not_found.html'


class InternalServerError(web.pages.Page):
    template = 'public/500.html'

