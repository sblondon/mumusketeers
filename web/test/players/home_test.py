import unittest.mock

import pytest
import transaction
import werkzeug.exceptions
import webtest

import models.games
import models.players
import web.application
import web.test.helper
import yzodb


class TestHome(web.test.helper.WebTestCase):

    def test(self):
        with yzodb.connection():
            player = models.players.create_player("test@domain.tld")
            transaction.commit()
            url = web.players.pages.Home.make_url(player)

        response = self.testapp.get(url, status=200)

        assert 'text/html' == response.content_type
        response.mustcontain('<!-- player home page -->')
        response.mustcontain(player.id)


def test_ghostify_another_player(testapp):
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player = game.add_player_email("player@domain.tld")
        target = game.add_player_email("target@domain.tld")
        game.start()
        transaction.commit()
        hunt = player.hunter_hunt_for_game(game)
        url = web.players.pages.Home.make_url(player)

    response = testapp.get(url, status=200)

    with unittest.mock.patch('mailings.request_confirm_ghostified') as request_confirm_ghostified:
        response.click(href=web.players.forms.GhostifyPlayer.make_url(game, player))

        request_confirm_ghostified.assert_called_once_with(game, hunt)
    with yzodb.connection():
        hunt = player.hunter_hunt_for_game(game)
        assert hunt.done_according_hunter
        assert False == hunt.done_according_target
    assert 'text/html' == response.content_type
    response.mustcontain('<!-- player home page -->')
    response.mustcontain(player.id)


def test_ghostified_by_another_player(testapp):
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player = game.add_player_email("player@domain.tld")
        target = game.add_player_email("target@domain.tld")
        game.start()
        transaction.commit()
        hunt = player.hunter_hunt_for_game(game)
        url = web.players.pages.Home.make_url(target)

    response = testapp.get(url, status=200)
    with unittest.mock.patch('mailings.request_confirm_ghostification') as request_confirm_ghostification:
        response.click(href=web.players.forms.GhostifiedPlayer.make_url(game, target))
        request_confirm_ghostification.assert_called_once_with(game, hunt)

    with yzodb.connection():
        hunt = target.hunted_hunt_for_game(game)
        assert False == hunt.done_according_hunter
        assert hunt.done_according_target
    assert 'text/html' == response.content_type
    response.mustcontain('<!-- player home page -->')
    response.mustcontain(target.id)

