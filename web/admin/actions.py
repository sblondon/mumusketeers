import ywsgi
import yzodb

import models.games
import models.players
import web.admin.pages
import web.admin.forms
import web.session
import web.strings
import web.players.forms
import web.players.pages


def connect(request, slugid=""):
    try:
        player = models.players.Player.read(slugid)
        web.session.login(player)
        return ywsgi.redirect(web.players.pages.Home.make_url(player))
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.LOGIN_ERROR)
    page = web.admin.pages.Players()
    return ywsgi.html(page.render())


@yzodb.commit
def create_user(request):
    form = web.admin.forms.CreatePlayer(request.form)
    if form.validate():
        player = models.players.create_player(form.email.data)
        web.session.add_user_success_notif(web.strings.USER_CREATE_SUCCESS.format(user=player.email))
        return ywsgi.redirect(web.admin.pages.Players.url)
    else:
        page = web.admin.pages.Players()
        page.form(form)
        web.session.add_user_error_notif(web.strings.USER_CREATE_FAILURE)
        return ywsgi.html(page.render())


@yzodb.commit
def delete_user(request, slugid=""):
    try:
        player = models.players.Player.read(slugid)
        player.delete()
        web.session.add_user_success_notif(web.strings.USER_DELETE_SUCCESS)
        return ywsgi.redirect(web.admin.pages.Players.url)
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_DELETE_FAILURE)
    page = web.admin.pages.Players()
    form = web.admin.forms.CreatePlayer()
    page.form(form)
    return ywsgi.html(page.render())


@yzodb.commit
def edit_user(request, slugid=""):
    try:
        player = models.players.Player.read(slugid)
        form = web.admin.forms.EditPlayer(request.form)
        if form.validate() or form.email.data == player.email:
            player.email  = form.email.data
            player.save()
            web.session.add_user_success_notif(web.strings.USER_EDIT_SUCCESS.format(user=player.email))
            return ywsgi.redirect(web.admin.pages.Players.url)
        else:
            web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
            page = web.admin.pages.EditPlayer()
            form.action = form.action + slugid
            page.form(form)
            page.user = player
            return ywsgi.html(page.render())

    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
    page = web.admin.pages.Players()
    form = web.admin.forms.CreatePlayer()
    page.form(form)
    return ywsgi.html(page.render())


@yzodb.commit
def create_game(request):
    form = web.admin.forms.CreateGame(request.form)
    if form.validate():
        game = models.games.create_game(form.name.data)
        web.session.add_user_success_notif(web.strings.GAME_CREATE_SUCCESS.format(name=game.name))
        return ywsgi.redirect(web.admin.pages.Games.url)
    else:
        page = web.admin.pages.Games()
        page.form(form)
        web.session.add_user_error_notif(web.strings.GAME_CREATE_FAILURE)
        return ywsgi.html(page.render())


@yzodb.commit
def edit_game(request, slugid=""):
    try:
        game = models.games.Game.read(slugid)
        form = web.admin.forms.EditGame(request.form)
        if form.validate() or True:
            game.name = form.name.data
            web.session.add_user_success_notif(web.strings.GAME_EDIT_SUCCESS.format(name=game.name))
            return ywsgi.redirect(web.admin.pages.Games.url)
#        else:
#            web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
#            page = web.admin.pages.EditPlayer()
#            form.action = form.action + slugid
#            page.form(form)
#            page.user = _user
#            return ywsgi.html(page.render())

    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
    page = web.admin.pages.Players()
    form = web.admin.forms.CreatePlayer()
    page.form(form)
    return ywsgi.html(page.render())


@yzodb.commit
def add_player_to_game(request):
    form = web.admin.forms.AddPlayerToGame(request.form)
    game = models.games.Game.read(form.game.data)
    player = game.add_player_email(form.email.data)
    web.session.add_user_success_notif(web.strings.PLAYER_ADDED_SUCCESS.format(player=player.email, game=game.name))
    return ywsgi.redirect(web.admin.pages.GameDetails.make_url(game))


@yzodb.commit
def start_game(request, slugid):
    game = models.games.Game.read(slugid)
    game.start()
    web.session.add_user_success_notif(web.strings.GAME_STARTED_SUCCESS)
    return ywsgi.redirect(web.admin.pages.GameDetails.make_url(game))

