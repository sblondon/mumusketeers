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


    def test_add_game(self):
        response = self.testapp.get(web.admin.pages.Games.url, status=200)
        response.mustcontain('No games')
        response.form.fields['name'][0].value = ' GAMENAME '

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            self.assertEqual("GAMENAME", game.name)
            response.mustcontain(game.id)
        response.mustcontain('GAMENAME')
        response.mustcontain(web.strings.GAME_CREATE_SUCCESS.format(name="GAMENAME"))


class TestGameDetails(web.tests.helper.WebTestCase):

    def test_change_all(self):
        with yzodb.connection():
            models.games.create_game('GAMENAME')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Games.url, status=200)

        response = response.click('Details')

        form = response.forms["update_game_form"]
        self.assertEqual(form.fields['name'][0].value, 'GAMENAME')
        form.fields['name'][0].value = 'New name'

        response = form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            self.assertEqual("New name", game.name)

        response.mustcontain(web.strings.GAME_EDIT_SUCCESS.format(name="New name"))


    def test_add_a_new_player(self):
        with yzodb.connection():
            game = models.games.create_game('GAMENAME')
            transaction.commit()
            url = web.admin.pages.GameDetails.make_url(game)

        response = self.testapp.get(url, status=200)

        form = response.forms["add_player_form"]
        form.fields['email'][0].value = "player@domain.tld"

        response = form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            player = models.users.read("player@domain.tld")
            self.assertIn(player, game.waiting_players)

        response.mustcontain(web.strings.PLAYER_ADDED_SUCCESS.format(player="player@domain.tld", game='GAMENAME'))

    def test_add_an_existing_player(self):
        EMAIL = 'player@domain.tld'
        with yzodb.connection():
            game = models.games.create_game('GAMENAME')
            player = models.users.create_player(EMAIL)
            transaction.commit()
            url = web.admin.pages.GameDetails.make_url(game)

        response = self.testapp.get(url, status=200)

        form = response.forms["add_player_form"]
        form.fields['email'][0].value = EMAIL

        response = form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            player = models.users.read(EMAIL)
            self.assertIn(player, game.waiting_players)
            self.assertEqual(1, models.users.Player.count())

        response.mustcontain(web.strings.PLAYER_ADDED_SUCCESS.format(player="player@domain.tld", game='GAMENAME'))


    def test_start_game(self):
        with yzodb.connection():
            game = models.games.create_game('GAMENAME')
            player_A = game.add_player_email("A@domain.tld")
            player_B = game.add_player_email("B@domain.tld")
            player_C = game.add_player_email("C@domain.tld")
            player_D = game.add_player_email("D@domain.tld")
            transaction.commit()
            url = web.admin.pages.GameDetails.make_url(game)
        response = self.testapp.get(url, status=200)

        response = response.click('Start game')
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            self.assertEqual(set(), set(game.waiting_players))
            self.assertEqual({player_A, player_B, player_C, player_D}, set(game.playing_players))

        response.mustcontain(web.strings.GAME_STARTED_SUCCESS)

