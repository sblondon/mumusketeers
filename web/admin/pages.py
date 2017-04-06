import models.players

import web.constantes
import web.pages


class AdminPage(web.pages.Page):

    @classmethod
    def make_url(cls, obj):
        return cls.url + "{0}".format(obj.id)


class Home(AdminPage):
    url = '/admin'
    url_regex = '^{0}/?$'.format(url)
    template = 'admin/index.html'


class Players(AdminPage):
    url = '/admin/players'
    url_regex = '^{0}$'.format(url)
    template = 'admin/users.html'

    def context_update(self):
        return dict(
            users=models.players.Player.read_all(),
            users_count=models.players.Player.count(),
        )


class EditPlayer(AdminPage):
    url = '/admin/player/edit/'
    url_regex = '^{url}(?P<slugid>{slugid})'.format(url=url, slugid=web.constantes.SLUGID_REGEX)
    template = 'admin/player_details.html'
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



class GameDetails(AdminPage):
    url = '/admin/games/'
    url_regex = '^{url}(?P<slugid>{slugid})'.format(url=url, slugid=web.constantes.SLUGID_REGEX)
    template = 'admin/game_details.html'

    def context_update(self):
        return dict(
            game=self.game,
            add_player_form=self.add_player_form,
        )

