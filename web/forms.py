import re
import wtforms

import models.users
import web.strings


def strip_filter(string):
    if string:
        return string.strip()


def user_email_unique_validator(form, field):
    if models.users.read(field.data):
        raise wtforms.ValidationError(web.strings.EMAIL_UNIQUE_ERROR)


def is_email_validator(form, field):
    mail_regex = """^[A-Z0-9._%+-]+                # myadress
                    @                              # @
                    [A-Z0-9.-]+                    # domainname
                    \.[A-Z]{2,13}$                 # .ext
                    """
    if not re.match(mail_regex, field.data.upper(), re.VERBOSE):
        raise wtforms.ValidationError(web.strings.EMAIL_FORMAT_ERROR)

