import yrouting
import ywsgi

import web.admin.pages
import web.admin.views
import web.admin.forms
import web.admin.actions

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.admin.views.home, web.admin.pages.Home.url_regex, 'GET')
ROUTER.add(web.admin.views.users, web.admin.pages.Players.url_regex, 'GET')
ROUTER.add(web.admin.views.edit_user, web.admin.pages.EditUser.url_regex,'GET')
ROUTER.add(web.admin.actions.create_user, web.admin.forms.CreateUser.action_regex, web.admin.forms.CreateUser.method)
ROUTER.add(lambda r: ywsgi.redirect(web.admin.pages.Players.url), web.admin.forms.CreateUser.action_regex, 'GET')
ROUTER.add(web.admin.actions.delete_user, web.admin.forms.DeleteUser.action_regex,'GET')
ROUTER.add(web.admin.actions.edit_user, web.admin.forms.EditUser.action_regex, web.admin.forms.EditUser.method)
ROUTER.add(web.admin.actions.connect, web.admin.forms.ConnectAsUser.action_regex, 'GET')

def get():
    return ROUTER

