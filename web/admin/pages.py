import models.users

import web.constantes
import web.pages


class AdminPage(web.pages.Page):
    pass


class Home(AdminPage):
    url = '/admin/'
    url_regex = '^{0}?$'.format(url)
    template = 'admin/index.html'


class Players(AdminPage):
    url = '/admin/players'
    url_regex = '^{0}$'.format(url)
    template = 'admin/users.html'

    def context_update(self):
        return dict(
            users=models.users.Player.read_all(),
            users_count=models.users.Player.count(),
        )


class EditPlayer(AdminPage):
    url = '/admin/player/edit/'
    url_regex = '^{url}(?P<uuid>{uuid})'.format(url=url, uuid=web.constantes.UUID_REGEX)
    template = 'admin/edit_users.html'
    _user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def context_update(self):
        return dict(
            user=self.user,
        )


class Games(AdminPage):
    url = '/admin/games'
    url_regex = '^{0}$'.format(url)
    template = 'admin/games.html'

    def context_update(self):
        return dict(
            games=models.games.Game.read_all(),
            games_count=models.games.Game.count(),
        )

