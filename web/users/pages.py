import web.pages
import web.session


class AbstractPage(web.pages.Page):
    def context_update(self):
        return {'user': web.session.user()}


class Home(AbstractPage):
    url = '/user/'
    url_regex = '^{0}$'.format(url)
    template = 'users/index.html'

