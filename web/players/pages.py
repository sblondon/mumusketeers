import web.constantes
import web.pages
import web.session


class AbstractPage(web.pages.Page):
    def context_update(self):
        return {'user': web.session.user()}

    @classmethod
    def make_url(cls, obj):
        return cls.url + "{0}".format(obj.id)


class Home(AbstractPage):
    url = '/player/'
    url_regex = '^{url}(?P<slugid>{slugid})'.format(url=url, slugid=web.constantes.SLUGID_REGEX)
    template = 'users/index.html'

    def context_update(self):
        print(self.player)
        return {"player": self.player}

