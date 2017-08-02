import web.constantes
import web.pages
import web.session
import web.settings


class AbstractPage(web.pages.Page):
    def context_update(self):
        return {'user': web.session.user()}

    @classmethod
    def make_url(cls, obj):
        return web.settings.HOST + cls.url + "{0}".format(obj.id)


class Home(AbstractPage):
    url = '/player/'
    url_regex = '^{url}(?P<slugid>{slugid})'.format(url=url, slugid=web.constantes.SLUGID_REGEX)
    template = 'players/index.html'

    def context_update(self):
        return {"player": self.player}

