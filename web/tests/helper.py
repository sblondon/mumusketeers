# -*- coding: utf-8 -*-

from datetime import datetime as Datetime
import webtest
import shutil

import yzodb

import web.application
import web.players.forms
import web.settings


class TestCase(yzodb.TestCase):
    pass


class WebTestCase(TestCase):

    def setUp(self):
        super(WebTestCase, self).setUp()
        self.application = web.application.make()
        self.testapp = webtest.TestApp(self.application)

    def tearDown(self):
        shutil.rmtree(web.settings.PERSISTENT_DIR)
        super(WebTestCase, self).tearDown()


class LoggedUserWebTestCase(WebTestCase):

    def setUp(self):
        super(LoggedUserWebTestCase, self).setUp()
        self.testapp.post('/admin/user/add/', dict(email='user@yaal.fr', password='password'))
        self.testapp.post(web.players.forms.Login.action, dict(email='user@yaal.fr', password='password'))

