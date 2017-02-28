import ywsgi

import web.users.pages
import web.session


def home(request):
    page = web.users.pages.Home()
    return ywsgi.html(page.render())

