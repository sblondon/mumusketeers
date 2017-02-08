import ywsgi

import web.users.forms
import web.users.pages
import web.session
import web.admin.pages
import web.public.pages


def logout(request):
    web.session.logout()
    web.session.add_user_success_notif(web.strings.LOGOUT_SUCCESS)
    return ywsgi.redirect(web.public.pages.Login.url)

