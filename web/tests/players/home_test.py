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


class TestGhostification(web.tests.helper.WebTestCase):
    def test_ghostify_another_player(self):
        with yzodb.connection():
            game = models.games.create_game("whatever")
            player = game.add_player_email("player@domain.tld")
            target = game.add_player_email("target@domain.tld")
            game.start()
            transaction.commit()
            url = web.players.pages.Home.make_url(player)

        response = self.testapp.get(url, status=200)
        response.click(href=web.players.forms.GhostifyPlayer.make_url(game, player))

        with yzodb.connection():
            hunt = player.hunter_hunt_for_game(game)
            assert hunt.done_according_hunter
            assert False == hunt.done_according_target
        assert 'text/html' == response.content_type
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)

    def test_ghostified_by_another_player(self):
        with yzodb.connection():
            game = models.games.create_game("whatever")
            player = game.add_player_email("player@domain.tld")
            target = game.add_player_email("target@domain.tld")
            game.start()
            transaction.commit()
            url = web.players.pages.Home.make_url(player)

        response = self.testapp.get(url, status=200)
        response.click(href=web.players.forms.GhostifiedPlayer.make_url(game, player))

        with yzodb.connection():
            hunt = player.hunted_hunt_for_game(game)
            assert False == hunt.done_according_hunter
            assert hunt.done_according_target
        assert 'text/html' == response.content_type
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)

