import wtforms
import web.forms


class Login(wtforms.Form):
    action = '/user/login/'
    action_regex = '^{0}$'.format(action)
    method = 'POST'

    email = wtforms.StringField(filters=[web.forms.strip_filter])
    password = wtforms.StringField()


class GetNewPassword(wtforms.Form):
    action = "/user/forgot-password"
    action_regex = '^{0}$'.format(action)

    email = wtforms.StringField(
            filters=[web.forms.strip_filter],
            validators=[wtforms.validators.Email()])
