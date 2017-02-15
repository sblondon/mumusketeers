import yrouting
import ywsgi

import web.admin.pages
import web.admin.views
import web.admin.forms
import web.admin.actions

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.admin.views.home, web.admin.pages.Home.url_regex, 'GET')
ROUTER.add(web.admin.views.users, web.admin.pages.Players.url_regex, 'GET')
ROUTER.add(web.admin.views.edit_user, web.admin.pages.EditPlayer.url_regex,'GET')
ROUTER.add(web.admin.actions.create_user, web.admin.forms.CreatePlayer.action_regex, web.admin.forms.CreatePlayer.method)
ROUTER.add(lambda r: ywsgi.redirect(web.admin.pages.Players.url), web.admin.forms.CreatePlayer.action_regex, 'GET')
ROUTER.add(web.admin.actions.delete_user, web.admin.forms.DeletePlayer.action_regex,'GET')
ROUTER.add(web.admin.actions.edit_user, web.admin.forms.EditPlayer.action_regex, web.admin.forms.EditPlayer.method)
ROUTER.add(web.admin.actions.connect, web.admin.forms.ConnectAsPlayer.action_regex, 'GET')

def get():
    return ROUTER

