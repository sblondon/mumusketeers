import yrouting

import web.users
import web.users.views
import web.users.pages
import web.users.forms
import web.users.actions
import web.session

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.users.actions.logout, '^/user/logout/$', 'GET')
ROUTER.add(web.users.views.home, web.users.pages.Home.url_regex, 'GET')


def get():
    def _app(request):
        user = web.session.user()
        if user:
            return ROUTER(request)
    return _app

