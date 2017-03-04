# -*- coding: utf-8 -*-

import transaction
import werkzeug.exceptions
import webtest

import models.players
import web.application
import web.tests.helper
import yzodb


class TestHome(web.tests.helper.WebTestCase):

    def test(self):
        with yzodb.connection():
            player = models.players.create_player("test@domain.tld")
            transaction.commit()
            url = web.players.pages.Home.make_url(player)

        response = self.testapp.get(url, status=200)

        self.assertEqual('text/html', response.content_type)
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)

