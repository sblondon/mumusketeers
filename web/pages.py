import ytemplates

import web.session


class Page(ytemplates.Template):

    def __init__(self):
        self._form = None

    def form(self, form):
        """ WTForm """
        self._form = form

    def global_context(self):
        cxt = {
                'user_notifs': web.session.pop_user_notifs(),
                'form': self._form,
               }
        cxt.update(self._static_context())
        return cxt

    def context_update(self):
        """ Méthode à redéfinir dans les classes filles """
        return {}

    def context(self):
        _context = self.global_context()
        _context.update(self.context_update())
        return _context

    @classmethod
    def _static_context(self):
        import web.players.forms
        return {
            "pages": {
                "admin": {
                    "Players": web.admin.pages.Players,
                    "Games": web.admin.pages.Games,
                    "GameDetails": web.admin.pages.GameDetails,
                },
            },
            "forms": {
                "admin": {
                    "ConnectAsPlayer": web.admin.forms.ConnectAsPlayer,
                    "DeletePlayer": web.admin.forms.DeletePlayer,
                    "EditPlayer": web.admin.forms.EditPlayer,
                    "StartGame": web.admin.forms.StartGame,
                },
            },
        }

