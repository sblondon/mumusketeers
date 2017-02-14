# -*- coding: utf-8 -*-

import web.tests.helper

import yzodb

import models.users
import web.strings


class TestAdminUsers(web.tests.helper.WebTestCase):

    def test_no_users_from_admin_home(self):
        response = self.testapp.get('/admin/', status=200)

        response = response.click('Players')

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')


    def test_add_user(self):
        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('Aucun utilisateur')
        response.form.fields['email'][0].value = 'user@yaal.fr '
        response.form.fields['password'][0].value = 'password'

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [_user] = models.users.User.read_all()
            self.assertTrue(_user.password_equals('password'))

        response.mustcontain('user@yaal.fr')
        response.mustcontain(web.strings.USER_CREATE_SUCCESS.format(user="user@yaal.fr"))


    def test_format_error_on_add_user(self):
        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('Aucun utilisateur')
        response.form.fields['email'][0].value = 'user@yaal'
        response.form.fields['password'][0].value = 'pass'

        response = response.form.submit(status=200)

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal')
        self.assertEquals(response.form.fields['password'][0].value, 'pass')
        response.mustcontain(web.strings.USER_CREATE_FAILURE)
        response.mustcontain(web.strings.EMAIL_FORMAT_ERROR)
        response.mustcontain(web.strings.PASSWORD_LENGTH_ERROR.format(length=6))


    def test_email_unique_error_on_add_user(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))
        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')
        response.form.fields['email'][0].value = 'user@yaal.fr'
        response.form.fields['password'][0].value = 'yaal and python for ever'

        response = response.form.submit(status=200)

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')
        self.assertEquals(response.form.fields['password'][0].value, 'yaal and python for ever')
        response.mustcontain(web.strings.USER_CREATE_FAILURE)
        response.mustcontain(web.strings.EMAIL_UNIQUE_ERROR)


    def test_redirect_on_get_url_add_user(self):
        response = self.testapp.get('/admin/user/add/', status=302)
        response = response.follow(status=200)

        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')


    def test_on_connect_as(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Connexion')
        response = response.follow(status=200)

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Accueil')


    def test_delete_user(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Supprimer')
        response = response.follow(status=200)

        response.mustcontain('Aucun utilisateur')
        response.mustcontain(web.strings.USER_DELETE_SUCCESS)


    def test_cannot_delete_user(self):
        response = self.testapp.get('/admin/user/del/12345678-1234-1234-1234-123456789012', status=200)

        response.mustcontain('Admin')
        response.mustcontain('Aucun utilisateur')
        response.mustcontain(web.strings.USER_DELETE_FAILURE)



class TestEditUser(web.tests.helper.WebTestCase):

    def test_change_all(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Modifier')

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')
        response.form.fields['email'][0].value = 'yop@yaal.fr'
        response.form.fields['password'][0].value = 'pastag'

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [_user] = models.users.User.read_all()
            self.assertTrue(_user.password_equals('pastag'))

        response.mustcontain(web.strings.USER_EDIT_SUCCESS.format(user="yop@yaal.fr"))

    def test_keep_email(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Modifier')

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        response.mustcontain(web.strings.USER_EDIT_SUCCESS.format(user="user@yaal.fr"))


    def test_keep_password(self):
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        response = response.click('Modifier')

        self.assertEquals(response.form.fields['email'][0].value, 'user@yaal.fr')

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [_user] = models.users.User.read_all()
            self.assertTrue(_user.password_equals('password'))

        response.mustcontain(web.strings.USER_EDIT_SUCCESS.format(user="user@yaal.fr"))


    def test_cannot_overwrite_other_user_email(self):
        self.testapp.post('/admin/user/add/', dict(email='previous_user@yaal.fr', password='password'))
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))

        response = self.testapp.get('/admin/users/', status=200)
        response.mustcontain('user@yaal.fr')

        with yzodb.connection():
            _user = models.users.read("user@yaal.fr")
        response = response.click('Modifier', href=_user.id)
        response.form.fields['email'][0].value = 'previous_user@yaal.fr'

        response = response.form.submit(status=200)

        response.mustcontain(web.strings.USER_EDIT_FAILURE)
        response.mustcontain(web.strings.EMAIL_UNIQUE_ERROR)

