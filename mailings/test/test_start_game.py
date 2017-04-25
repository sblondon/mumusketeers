import transaction
import yzodb

import web.settings
import models.games
import mailings.test

send_called = 0


class MailServer(mailings.test.AbstractMailServer):
    def check(self, markdownmail):
        super(MailServer, self).check(markdownmail)
        global send_called
        send_called += 1
        assert markdownmail.to_addr[0] in ("player-1@domain.tld", "player-2@domain.tld")


def test_start(init_ytemplates):
    SMTP_SERVER = web.settings.SMTP_SERVER
    try:
        web.settings.SMTP_SERVER = MailServer()
        with yzodb.connection():
            game = models.games.create_game("whatever")
            player_1 = game.add_player_email("player-1@domain.tld")
            player_2 = game.add_player_email("player-2@domain.tld")
            game.start()
            transaction.commit()
 
        assert send_called == 2
    finally:
        web.settings.SMTP_SERVER = SMTP_SERVER

