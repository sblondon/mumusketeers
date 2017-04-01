import ywsgi
import yzodb

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
    hunt = player.hunter_hunt_for_game(game)
    hunt.done_according_hunter = True
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

@yzodb.commit
def ghostified_player(request, game_id, player_id):
    game = models.games.Game.read(game_id)
    player = models.players.Player.read(player_id)
    hunt = player.hunted_hunt_for_game(game)
    hunt.done_according_target = True
    return ywsgi.redirect(web.players.pages.Home.make_url(player))
    return ywsgi.redirect(web.players.pages.Home.make_url(player))

