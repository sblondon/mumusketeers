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
        response.mustcontain('Ready to ghostify?')


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

