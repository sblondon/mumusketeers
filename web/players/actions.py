import ywsgi

import models.players
import web.players.forms
import web.players.pages
import web.session
import web.admin.pages
import web.public.pages


def logout(request):
    web.session.logout()
    web.session.add_user_success_notif(web.strings.LOGOUT_SUCCESS)
    return ywsgi.redirect(web.public.pages.Login.url)

def ghostify_player(request, game_id, player_id):
    player = models.players.Player.read(player_id)
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

def ghostified_player(request, game_id, player_id):
    player = models.players.Player.read(player_id)
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

