# -*- coding: utf-8 -*-

import web.tests.helper

class TestAdminHome(web.tests.helper.WebTestCase):

    def test(self):
        _response = self.testapp.get('/admin/', status=200)

        assert 'text/html' == _response.content_type
        _response.mustcontain('Admin')

    def test_without_trailing_slash(self):
        _response = self.testapp.get('/admin', status=200)

        assert 'text/html' == _response.content_type
        _response.mustcontain('Admin')

