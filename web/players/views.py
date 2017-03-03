import ywsgi

import web.players.pages
import web.session


def home(request):
    page = web.players.pages.Home()
    return ywsgi.html(page.render())

