# -*- coding: utf-8 -*-
import transaction

import web.tests.helper

import yzodb

import models.users
import web.strings
import web.admin.pages
import web.admin.forms


class TestAdminGames(web.tests.helper.WebTestCase):

    def test_no_games_from_admin_home(self):
        response = self.testapp.get(web.admin.pages.Home.url, status=200)

        response = response.click('Games')

        self.assertEquals('text/html', response.content_type)
        response.mustcontain('Admin')
        response.mustcontain('No games')
