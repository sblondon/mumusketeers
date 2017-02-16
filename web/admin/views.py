import ywsgi

import models.users

import web.admin.pages
import web.admin.forms


def home(request):
    _page = web.admin.pages.Home()
    return ywsgi.html(_page.render())


def users(request):
    _page = web.admin.pages.Players()
    _page.form(web.admin.forms.CreatePlayer())
    return ywsgi.html(_page.render())


def edit_user(request, uuid=""):
    _user = models.users.Player.read(uuid)
    _page = web.admin.pages.EditPlayer()
    _page.user = _user
    _form = web.admin.forms.EditPlayer()
    _form.email.raw_data = [_user.email]
    _form.action = _form.action + uuid
    _page.form(_form)
    return ywsgi.html(_page.render())


def games(request):
    _page = web.admin.pages.Games()
    return ywsgi.html(_page.render())

