import yrouting
import ywsgi

import web.public.actions
import web.public.forms
import web.public.pages
import web.public.views

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.public.views.home, web.public.pages.Home.url_regex, 'GET')
ROUTER.add(web.public.actions.login, web.public.forms.Login.action_regex, web.public.forms.Login.method)
ROUTER.add(web.public.actions.get_new_password, web.public.forms.GetNewPassword.action_regex, 'POST')
ROUTER.add(lambda r: ywsgi.redirect(web.public.pages.Login.url), web.public.forms.Login.action_regex, 'GET')


def get():
    return ROUTER

