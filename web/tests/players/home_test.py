# -*- coding: utf-8 -*-

import transaction
import werkzeug.exceptions
import webtest

import models.games
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

        assert 'text/html' == response.content_type
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)

    def test_ghostify_another_player(self):
        with yzodb.connection():
            game = models.games.create_game("whatever")
            player = game.add_player_email("player@domain.tld")
            target = game.add_player_email("target@domain.tld")
            game.start()
            transaction.commit()
            url = web.players.pages.Home.make_url(player)

        response = self.testapp.get(url, status=200)
        response.click(web.players.forms.GhostifyPlayer.make_url(game, player)) #, status=302)
        response = response.follow()

        assert 'text/html' == response.content_type
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)

