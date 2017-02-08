import wtforms

import web.constantes
import web.forms
import web.strings



class CreateUser(wtforms.Form):
    action = '/admin/user/add/'
    action_regex = '^{0}$'.format(action)
    method = 'POST'
    MIN_PASSWORD_LENGTH = 6

    email = wtforms.StringField(
            validators=[
                web.forms.user_email_unique_validator,
                web.forms.is_email_validator,
                ],
            filters=[web.forms.strip_filter]
            )
    password = wtforms.StringField("Modifier le mot de passe (reste inchangé si vide)",
            validators=[wtforms.validators.Length(
                min=MIN_PASSWORD_LENGTH,
                message=web.strings.PASSWORD_LENGTH_ERROR.format(length=MIN_PASSWORD_LENGTH)
                )]
            )


class EditUser(wtforms.Form):
    action = '/admin/user/edit/'
    action_regex = '^{0}(?P<uuid>{uuid})$'.format(action, uuid=web.constantes.UUID_REGEX)
    method = 'POST'
    MIN_PASSWORD_LENGTH = 6

    email = wtforms.StringField(
            validators=[
                web.forms.user_email_unique_validator,
                web.forms.is_email_validator,
                ],
            filters=[web.forms.strip_filter]
            )
    password = wtforms.StringField(
            validators=[wtforms.validators.Length(
                min=MIN_PASSWORD_LENGTH,
                message=web.strings.PASSWORD_LENGTH_ERROR.format(length=MIN_PASSWORD_LENGTH)
                )]
            )

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   


class DeleteUser(wtforms.Form):
    action = '/admin/user/del/'
    action_regex = '^{action}(?P<uuid>{uuid})$'.format(action=action, uuid=web.constantes.UUID_REGEX)

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   


class ConnectAsUser(wtforms.Form):
    action = '/admin/user/connect/'
    action_regex = '^{action}(?P<uuid>{uuid})$'.format(action=action, uuid=web.constantes.UUID_REGEX)

    @classmethod
    def make_url(cls, user):
        return cls.action+"{0}".format(user.id)   

