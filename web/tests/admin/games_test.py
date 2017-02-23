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

        self.assertEquals(response.form.fields['name'][0].value, 'GAMENAME')
        response.form.fields['name'][0].value = 'New name'

        response = response.form.submit(status=302)
        response = response.follow(status=200)

        with yzodb.connection():
            [game] = models.games.Game.read_all()
            self.assertEqual("New name", game.name)

        response.mustcontain(web.strings.GAME_EDIT_SUCCESS.format(name="New name"))

