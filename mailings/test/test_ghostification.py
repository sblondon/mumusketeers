import transaction
import yzodb

import web.settings
import models.games
import mailings
import mailings.test

ghostified_send_call_count = 0
ghostify_send_call_count = 0


class GhostifiedMailServer(mailings.test.AbstractMailServer):
    def check(self, markdownmail):
        super(GhostifiedMailServer, self).check(markdownmail)
        global ghostified_send_call_count
        ghostified_send_call_count += 1
        assert markdownmail.to_addr[0] == "player-2@domain.tld"


def test_request_confirm_ghostified(init_ytemplates):
    SMTP_SERVER = web.settings.SMTP_SERVER
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        game.start()
        hunt = player_1.hunter_hunt_for_game(game)
        transaction.commit()

    try:
        web.settings.SMTP_SERVER = GhostifiedMailServer()
        with yzodb.connection():
            mailings.request_confirm_ghostified(game, hunt)
 
        assert ghostified_send_call_count == 1
    finally:
        web.settings.SMTP_SERVER = SMTP_SERVER


class GhostifyMailServer(mailings.test.AbstractMailServer):
    def check(self, markdownmail):
        super(GhostifyMailServer, self).check(markdownmail)
        global ghostify_send_call_count
        ghostify_send_call_count += 1
        assert markdownmail.to_addr[0] == "player-1@domain.tld"


def test_request_confirm_ghostification(init_ytemplates):
    SMTP_SERVER = web.settings.SMTP_SERVER
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        game.start()
        hunt = player_1.hunter_hunt_for_game(game)
        transaction.commit()

    try:
        web.settings.SMTP_SERVER = GhostifyMailServer()
        with yzodb.connection():
            mailings.request_confirm_ghostification(game, hunt)
 
        assert ghostify_send_call_count == 1
    finally:
        web.settings.SMTP_SERVER = SMTP_SERVER

