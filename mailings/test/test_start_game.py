import markdownmail
import transaction
import yzodb

import web.settings
import models.games


server_called = 0

class MailServer(markdownmail.NullServer):
    def send(self, markdownmail):
        server_called += 1
        assert markdownmail.to_addr in ("player-1@domain.tld", "player-2@domain.tld")



def test_start():
    SMTP_SERVER = web.settings.SMTP_SERVER
    web.settings.SMTP_SERVER = MailServer()
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        game.start()
        transaction.commit()

    assert server_called == 2

    web.settings.SMTP_SERVER = SMTP_SERVER

