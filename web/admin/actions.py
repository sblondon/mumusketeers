# -*- coding: utf-8 -*-
import ywsgi
import yzodb

import models.games
import models.users
import web.admin.pages
import web.admin.forms
import web.session
import web.strings
import web.users.forms
import web.users.pages


def connect(request, slugid=""):
    try:
        _user = models.users.Player.read(slugid)
        web.session.login(_user)
        return ywsgi.redirect(web.users.pages.Home.url)
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.LOGIN_ERROR)
    _page = web.admin.pages.Players()
    return ywsgi.html(_page.render())


@yzodb.commit
def create_user(request):
    _form = web.admin.forms.CreatePlayer(request.form)
    if _form.validate():
        _user = models.users.create(_form.email.data)
        web.session.add_user_success_notif(web.strings.USER_CREATE_SUCCESS.format(user=_user.email))
        return ywsgi.redirect(web.admin.pages.Players.url)
    else:
        _page = web.admin.pages.Players()
        _page.form(_form)
        web.session.add_user_error_notif(web.strings.USER_CREATE_FAILURE)
        return ywsgi.html(_page.render())


@yzodb.commit
def delete_user(request, slugid=""):
    try:
        _user = models.users.Player.read(slugid)
        _user.delete()
        web.session.add_user_success_notif(web.strings.USER_DELETE_SUCCESS)
        return ywsgi.redirect(web.admin.pages.Players.url)
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_DELETE_FAILURE)
    _page = web.admin.pages.Players()
    _form = web.admin.forms.CreatePlayer()
    _page.form(_form)
    return ywsgi.html(_page.render())


@yzodb.commit
def edit_user(request, slugid=""):
    try:
        _user = models.users.Player.read(slugid)
        _form = web.admin.forms.EditPlayer(request.form)
        if _form.validate() or _form.email.data == _user.email:
            _user.email  = _form.email.data
            _user.save()
            web.session.add_user_success_notif(web.strings.USER_EDIT_SUCCESS.format(user=_user.email))
            return ywsgi.redirect(web.admin.pages.Players.url)
        else:
            web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
            _page = web.admin.pages.EditPlayer()
            _form.action = _form.action + slugid
            _page.form(_form)
            _page.user = _user
            return ywsgi.html(_page.render())

    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
    _page = web.admin.pages.Players()
    _form = web.admin.forms.CreatePlayer()
    _page.form(_form)
    return ywsgi.html(_page.render())


@yzodb.commit
def create_game(request):
    form = web.admin.forms.CreateGame(request.form)
    if form.validate():
        game = models.games.create_game(form.name.data)
        web.session.add_user_success_notif(web.strings.GAME_CREATE_SUCCESS.format(name=game.name))
        return ywsgi.redirect(web.admin.pages.Games.url)
    else:
        _page = web.admin.pages.Players()
        _page.form(_form)
        web.session.add_user_error_notif(web.strings.USER_CREATE_FAILURE)
        return ywsgi.html(_page.render())


@yzodb.commit
def edit_game(request, slugid=""):
    try:
        game = models.games.Game.read(slugid)
        _form = web.admin.forms.EditGame(request.form)
        if _form.validate() or True:
            game.name = _form.name.data
            web.session.add_user_success_notif(web.strings.GAME_EDIT_SUCCESS.format(name=game.name))
            return ywsgi.redirect(web.admin.pages.Games.url)
#        else:
#            web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
#            _page = web.admin.pages.EditPlayer()
#            _form.action = _form.action + slugid
#            _page.form(_form)
#            _page.user = _user
#            return ywsgi.html(_page.render())

    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
    _page = web.admin.pages.Players()
    _form = web.admin.forms.CreatePlayer()
    _page.form(_form)
    return ywsgi.html(_page.render())

