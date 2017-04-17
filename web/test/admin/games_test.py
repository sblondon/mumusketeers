import unittest.mock

import transaction

import web.test.helper

import yzodb

import models.players
import web.strings
import web.admin.pages
import web.admin.forms


class TestAdminGames(web.test.helper.WebTestCase):

    def test_no_games_from_admin_home(self):
        response = self.testapp.get(web.admin.pages.Home.url, status=200)

        response = response.click('Games')

        assert 'text/html' == response.content_type
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
            assert "GAMENAME" == game.name
            response.mustcontain(game.id)
        response.mustcontain('GAMENAME')
        response.mustcontain(web.strings.GAME_CREATE_SUCCESS.format(name="GAMENAME"))


    def test_add_game_error(self):
        response = self.testapp.get(web.admin.pages.Games.url, status=200)
        response.mustcontain('No games')
        response.form.fields['name'][0].value = 'A' * (web.admin.forms.CreateGame.MIN_NAME_LENGTH - 1)

        response = response.form.submit(status=200)

        with yzodb.connection():
            assert 0 == models.games.Game.count()
        response.mustcontain(web.strings.GAME_CREATE_FAILURE)


class TestGameDetails(web.test.helper.WebTestCase):

    def test_change_all(self):
        with yzodb.connection():
            models.games.create_game('GAMENAME')
            transaction.commit()

        response = self.testapp.get(web.admin.pages.Games.url, status=200)

        response = response.click('Details')

        form = response.forms["update_game_form"]
        assert form.fields['name'][0].value == 'GAMENAME'
        form.fields['name'][0].value = 'New name'

        response = form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            assert "New name" == game.name

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
            player = models.players.read("player@domain.tld")
            assert player in game.waiting_players

        response.mustcontain(web.strings.PLAYER_ADDED_SUCCESS.format(player="player@domain.tld", game='GAMENAME'))

    def test_add_an_existing_player(self):
        EMAIL = 'player@domain.tld'
        with yzodb.connection():
            game = models.games.create_game('GAMENAME')
            player = models.players.create_player(EMAIL)
            transaction.commit()
            url = web.admin.pages.GameDetails.make_url(game)

        response = self.testapp.get(url, status=200)

        form = response.forms["add_player_form"]
        form.fields['email'][0].value = EMAIL

        response = form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            player = models.players.read(EMAIL)
            assert player in game.waiting_players
            assert 1 == models.players.Player.count()
            assert game in player.wait_for_games
            assert game in player.games

        response.mustcontain(web.strings.PLAYER_ADDED_SUCCESS.format(player="player@domain.tld", game='GAMENAME'))

    @unittest.mock.patch("mailings.start_game")
    def test_start_game(self, mailings_start_game):
        with yzodb.connection():
            game = models.games.create_game('GAMENAME')
            player_A = game.add_player_email("A@domain.tld")
            player_B = game.add_player_email("B@domain.tld")
            player_C = game.add_player_email("C@domain.tld")
            player_D = game.add_player_email("D@domain.tld")
            transaction.commit()
            url = web.admin.pages.GameDetails.make_url(game)
            assert game.preparing
            assert not game.running
        response = self.testapp.get(url, status=200)

        response = response.click('Start game')
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            assert not game.preparing
            assert game.running
            assert set() == set(game.waiting_players)
            assert {player_A, player_B, player_C, player_D} == set(game.playing_players)
            current_targets = set()
            targetted_by_players = set()
            for player in game.playing_players:
                assert player.current_target_for_game(game) in game.playing_players
                assert player.current_target_for_game(game) != player
                current_targets.add(player.current_target_for_game(game))
                assert player.targetted_by_player_for_game(game) in game.playing_players
                assert player.targetted_by_player_for_game(game) != player
                targetted_by_players.add(player.targetted_by_player_for_game(game))
                assert game in player.games
                assert game not in player.wait_for_games
            assert {player_A, player_B, player_C, player_D} == current_targets
            assert {player_A, player_B, player_C, player_D} == targetted_by_players
            assert {player_A, player_B, player_C, player_D} == set(game.players_loop)
        mailings_start_game.assert_called_once_with(game)

        response.mustcontain(web.strings.GAME_STARTED_SUCCESS)
        response.mustcontain(no=['Start game'])

