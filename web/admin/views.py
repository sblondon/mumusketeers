import ywsgi

import models.users

import web.admin.pages
import web.admin.forms


def home(request):
    page = web.admin.pages.Home()
    return ywsgi.html(page.render())


def users(request):
    page = web.admin.pages.Players()
    page.form(web.admin.forms.CreatePlayer())
    return ywsgi.html(page.render())


def edit_user(request, slugid=""):
    player = models.users.Player.read(slugid)
    page = web.admin.pages.EditPlayer()
    page.user = player
    form = web.admin.forms.EditPlayer()
    form.email.raw_data = [player.email]
    form.action = form.action + slugid
    page.form(form)
    return ywsgi.html(page.render())


def games(request):
    page = web.admin.pages.Games()
    page.form(web.admin.forms.CreateGame())
    return ywsgi.html(page.render())


def game_details(request, slugid):
    game = models.games.Game.read(slugid)
    page = web.admin.pages.GameDetails()
    page.game = game
    form = web.admin.forms.EditGame()
    form.name.raw_data = [game.name]
    form.action = form.action + slugid
    page.form(form)
    add_player_form = web.admin.forms.AddPlayerToGame()
    add_player_form.game.data = game.id
    page.add_player_form = add_player_form
    return ywsgi.html(page.render())

