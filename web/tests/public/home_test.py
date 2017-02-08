# -*- coding: utf-8 -*-

import transaction
import werkzeug.exceptions
import webtest

import models.users
import web.application
import web.tests.helper
import yzodb


class TestHome(web.tests.helper.WebTestCase):

    def test(self):
        response = self.testapp.get('/', status=200)

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Bienvenue')


class TestMotDePasseOublie(web.tests.helper.WebTestCase):

    def test(self):
        with yzodb.connection():
             self.user = models.users.create("user@yopmail.fr", "motdepasse")
             old_encrypted_password = self.user.password
             transaction.commit()

        self.testapp.post(
                web.public.forms.GetNewPassword.action,
                {"email": 'user@yopmail.fr'},
                status=200)

        with yzodb.connection():
             updated_user = models.users.read("user@yopmail.fr")
             self.assertNotEqual(updated_user.password, old_encrypted_password)

    def test_ne_rien_signaler_si_le_compte_n_existe_pas(self):
        self.testapp.post(
                web.public.forms.GetNewPassword.action,
                {"email": 'user@yopmail.fr'},
                status=200)

    def test_erreur_si_n_est_pas_un_email(self):
        response = self.testapp.post(
                web.public.forms.GetNewPassword.action,
                {"email": 'user'},
                status=400)

        self.assertEqual(
            {"email": ['Invalid email address.']},
            response.json["errors"])


class Test404(web.tests.helper.WebTestCase):

    def test(self):
        response = self.testapp.get('/this-url-does-not-exist', status=404)

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('404')


class TestBadRequest(web.tests.helper.TestCase):
    def test_debug(self):
        PreviousApp = web.application.YApp
        class BadRequestApp(object):
            def __call__(self, request):
                return werkzeug.exceptions.BadRequest()
        web.application.YApp = BadRequestApp
        self.application = web.application.make()
        self.testapp = webtest.TestApp(self.application)

        response = self.testapp.get('/', status=500)

        response.mustcontain("BadRequest")

        web.application.YApp = PreviousApp

