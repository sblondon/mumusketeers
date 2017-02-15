import rstr
import ywsgi

import models.users
import yzodb
import web.public.pages
import web.session
import web.admin.forms
import web.users.forms
import web.users.pages
import web.public.forms


def login(request):
    form = web.public.forms.Login(request.form)
    user = models.users.authenticate(form.email.data, form.password.data)
    if user:
        web.session.login(user)
        web.session.add_user_success_notif(
                web.strings.LOGIN_SUCCESS.format(user=form.email.data))
        return ywsgi.redirect(web.users.pages.Home.url)
    else:
        web.session.add_user_error_notif(web.strings.LOGIN_ERROR)
    page = web.public.pages.Login()
    page.form(form)
    return ywsgi.html(page.render())


@yzodb.commit
def get_new_password(request):
    """TODO: adapter la réponse au service souhaité (page, JSON, etc.)""" 
    form = web.public.forms.GetNewPassword(request.form)
    if form.validate():
        user = models.users.read(form.email.data)
        if user:
            password = rstr.domainsafe(
                web.admin.forms.CreatePlayer.MIN_PASSWORD_LENGTH,
                exclude=["-", "0", "1", "O", "l"])
            user.password = password
        return ywsgi.html("Bravo")
    else:
        return ywsgi.json({"errors": form.errors}, status=400)

