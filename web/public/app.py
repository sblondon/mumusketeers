import yrouting

import web.public.pages
import web.public.views

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.public.views.home, web.public.pages.Home.url_regex, 'GET')


def get():
    return ROUTER

