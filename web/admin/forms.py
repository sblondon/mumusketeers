import wtforms

import web.constantes
import web.forms
import web.strings



class CreatePlayer(wtforms.Form):
    action = '/admin/player/add'
    action_regex = '^{0}$'.format(action)
    method = 'POST'

    email = wtforms.StringField(
            validators=[
                web.forms.user_email_unique_validator,
                web.forms.is_email_validator,
                ],
            filters=[web.forms.strip_filter]
            )


class EditPlayer(wtforms.Form):
    action = '/admin/player/edit/'
    action_regex = '^{0}(?P<slugid>{slugid})$'.format(action, slugid=web.constantes.SLUGID_REGEX)
    method = 'POST'

    email = wtforms.StringField(
            validators=[
                web.forms.user_email_unique_validator,
                web.forms.is_email_validator,
                ],
            filters=[web.forms.strip_filter]
            )

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   


class DeletePlayer(wtforms.Form):
    action = '/admin/player/delete/'
    action_regex = '^{0}(?P<slugid>{slugid})$'.format(action, slugid=web.constantes.SLUGID_REGEX)

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   


class ConnectAsPlayer(wtforms.Form):
    action = '/admin/player/connect/'
    action_regex = '^{0}(?P<slugid>{slugid})$'.format(action, slugid=web.constantes.SLUGID_REGEX)

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   


class CreateGame(wtforms.Form):
    action = '/admin/game/add'
    action_regex = '^{0}$'.format(action)
    method = 'POST'
    MIN_NAME_LENGTH = 4

    name = wtforms.StringField(
            validators=[wtforms.validators.Length(min=MIN_NAME_LENGTH)],
            filters=[web.forms.strip_filter]
            )


class EditGame(wtforms.Form):
    action = '/admin/game/edit/'
    action_regex = '^{0}(?P<slugid>{slugid})$'.format(action, slugid=web.constantes.SLUGID_REGEX)
    method = 'POST'
    MIN_NAME_LENGTH = 4

    name = wtforms.StringField(
            validators=[wtforms.validators.Length(min=MIN_NAME_LENGTH)],
            filters=[web.forms.strip_filter]
            )

class AddPlayerToGame(wtforms.Form):
    action = '/admin/game/player/add'
    action_regex = '^{0}$'.format(action)
    method = 'POST'

    game = wtforms.HiddenField()
    email = wtforms.StringField(
            validators=[
                web.forms.user_email_unique_validator,
                web.forms.is_email_validator,
                ],
            filters=[web.forms.strip_filter]
            )

