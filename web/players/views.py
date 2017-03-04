import ywsgi

import models.players
import web.players.pages
import web.session


def home(request, slugid):
    player = models.players.Player.read(slugid)
    page = web.players.pages.Home()
    page.player = player
    return ywsgi.html(page.render())

