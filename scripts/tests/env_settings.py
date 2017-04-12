import markdownmail

import web.settings

web.settings.SMTP_SERVER = markdownmail.NullServer()

