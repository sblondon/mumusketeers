import yrouting

import web.players
import web.players.views
import web.players.pages
import web.players.forms
import web.players.actions
import web.session

ROUTER = yrouting.RegexRouter()

ROUTER.add(web.players.actions.logout, '^/user/logout/$', 'GET')
ROUTER.add(web.players.views.home, web.players.pages.Home.url_regex, 'GET')
ROUTER.add(web.players.actions.ghostify_player, web.players.forms.GhostifyPlayer.action_regex, 'GET')


def get():
    def _app(request):
        print(request.path)
        return ROUTER(request)
    return _app

