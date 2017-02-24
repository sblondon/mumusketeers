# -*- coding: utf-8 -*-
import transaction

import web.tests.helper

import yzodb

import models.users
import web.strings
import web.admin.pages
import web.admin.forms


class TestAdminPlayers(web.tests.helper.WebTestCase):

    def test_no_users_from_admin_home(self):
        response = self.testapp.get(web.admin.pages.Home.url, status=200)

        response = response.click('Players')

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')


    def test_add_user(self):
        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('Aucun utilisateur')
        response.form.fields['email'][0].value = 'user@yaal.fr '

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [_user] = models.users.Player.read_all()
            self.assertTrue("user@yaal.fr", _user.email)

        response.mustcontain('user@yaal.fr')
        response.mustcontain(web.strings.USER_CREATE_SUCCESS.format(user="user@yaal.fr"))


    def test_format_error_on_add_user(self):
        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('Aucun utilisateur')
        response.form.fields['email'][0].value = 'user@yaal'

        response = response.form.submit(status=200)

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal')
        response.mustcontain(web.strings.USER_CREATE_FAILURE)
        response.mustcontain(web.strings.EMAIL_FORMAT_ERROR)


    def test_email_unique_error_on_add_user(self):
        with yzodb.connection():
            models.users.create('user@yaal.fr')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')
        response.form.fields['email'][0].value = 'user@yaal.fr'

        response = response.form.submit(status=200)

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')
        response.mustcontain(web.strings.USER_CREATE_FAILURE)


    def test_redirect_on_get_url_add_user(self):
        response = self.testapp.get(web.admin.forms.CreatePlayer.action, status=302)
        response = response.follow(status=200)

        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')


    def test_on_connect_as(self):
        with yzodb.connection():
            models.users.create('user@yaal.fr')
            transaction.commit()
        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Connexion')
        response = response.follow(status=200)

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Accueil')


    def test_delete_user(self):
        with yzodb.connection():
            models.users.create('user@yaal.fr')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Supprimer')
        response = response.follow(status=200)

        response.mustcontain('Aucun utilisateur')
        response.mustcontain(web.strings.USER_DELETE_SUCCESS)


    def test_cannot_delete_user(self):
        class FakePlayer:
            id = models.users.Player.propose_id()
        response = self.testapp.get(web.admin.forms.DeletePlayer.make_url(FakePlayer()), status=200)

        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')
        response.mustcontain(web.strings.USER_DELETE_FAILURE)



class TestEditPlayer(web.tests.helper.WebTestCase):

    def test_change_all(self):
        with yzodb.connection():
            models.users.create('user@yaal.fr')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Modifier')

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')
        response.form.fields['email'][0].value = 'yop@yaal.fr'

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [_user] = models.users.Player.read_all()

        response.mustcontain(web.strings.USER_EDIT_SUCCESS.format(user="yop@yaal.fr"))

    def test_keep_email(self):
        with yzodb.connection():
            models.users.create('user@yaal.fr')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Modifier')

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        response.mustcontain(web.strings.USER_EDIT_SUCCESS.format(user="user@yaal.fr"))


    def test_cannot_overwrite_other_user_email(self):
        with yzodb.connection():
            models.users.create('previous_user@yaal.fr')
            models.users.create('user@yaal.fr')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Players.url, status=200)
        response.mustcontain('user@yaal.fr')

        with yzodb.connection():
            _user = models.users.read("user@yaal.fr")
        response = response.click('Modifier', href=_user.id)
        response.form.fields['email'][0].value = 'previous_user@yaal.fr'

        response = response.form.submit(status=200)

        response.mustcontain(web.strings.USER_EDIT_FAILURE)
        response.mustcontain(web.strings.EMAIL_UNIQUE_ERROR)

