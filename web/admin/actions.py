# -*- coding: utf-8 -*-
import ywsgi
import yzodb

import models.users
import web.admin.pages
import web.admin.forms
import web.session
import web.strings
import web.users.forms
import web.users.pages


def connect(request, uuid=""):
    try:
        _user = models.users.User.read(uuid)
        web.session.login(_user)
        return ywsgi.redirect(web.users.pages.Home.url)
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.LOGIN_ERROR)
    _page = web.admin.pages.Users()
    return ywsgi.html(_page.render())


@yzodb.commit
def create_user(request):
    _form = web.admin.forms.CreateUser(request.form)
    if _form.validate():
        _user = models.users.create(_form.email.data, _form.password.data)
        web.session.add_user_success_notif(web.strings.USER_CREATE_SUCCESS.format(user=_user.email))
        return ywsgi.redirect(web.admin.pages.Users.url)
    else:
        _page = web.admin.pages.Users()
        _page.form(_form)
        web.session.add_user_error_notif(web.strings.USER_CREATE_FAILURE)
        return ywsgi.html(_page.render())


@yzodb.commit
def delete_user(request, uuid=""):
    try:
        _user = models.users.User.read(uuid)
        _user.delete()
        web.session.add_user_success_notif(web.strings.USER_DELETE_SUCCESS)
        return ywsgi.redirect(web.admin.pages.Users.url)
    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_DELETE_FAILURE)
    _page = web.admin.pages.Users()
    _form = web.admin.forms.CreateUser()
    _page.form(_form)
    return ywsgi.html(_page.render())


@yzodb.commit
def edit_user(request, uuid=""):
    try:
        _user = models.users.User.read(uuid)
        _form = web.admin.forms.EditUser(request.form)
        if _form.validate() or _form.email.data == _user.email:
            _user.email  = _form.email.data
            if _form.password.data:
                _user.password = _form.password.data
            _user.save()
            web.session.add_user_success_notif(web.strings.USER_EDIT_SUCCESS.format(user=_user.email))
            return ywsgi.redirect(web.admin.pages.Users.url)
        else:
            web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
            _page = web.admin.pages.EditUser()
            _form.action = _form.action + uuid
            _page.form(_form)
            _page.user = _user
            return ywsgi.html(_page.render())

    except yzodb.ObjectNotFoundException:
        web.session.add_user_error_notif(web.strings.USER_EDIT_FAILURE)
    _page = web.admin.pages.Users()
    _form = web.admin.forms.CreateUser()
    _page.form(_form)
    return ywsgi.html(_page.render())

