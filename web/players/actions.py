import ywsgi
import yzodb

import mailings
import models.games
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

@yzodb.commit
def ghostify_player(request, game_id, player_id):
    game = models.games.Game.read(game_id)
    player = models.players.Player.read(player_id)
    player.declare_ghostify_for_game(game)
    hunt = player.hunter_hunt_for_game(game)
    mailings.request_confirm_ghostified(game, hunt)
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

@yzodb.commit
def ghostified_player(request, game_id, player_id):
    game = models.games.Game.read(game_id)
    player = models.players.Player.read(player_id)
    player.declare_ghostified_for_game(game)
    hunt = player.hunted_hunt_for_game(game)
    mailings.request_confirm_ghostification(game, hunt)
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

