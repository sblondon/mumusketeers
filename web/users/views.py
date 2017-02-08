import ywsgi

import web.users.pages
import web.session


def home(request):
    _page = web.users.pages.Home()
    return ywsgi.html(_page.render())

