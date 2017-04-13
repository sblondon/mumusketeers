import markdownmail

import web.settings


def start_game(game):
    for player in game.playing_players:
        email = markdownmail.MarkdownMail(
                from_addr="noreply@changeme.tld",
                to_addr=player.email,
                subject="Game starts",
                content="CONTENT")
        email.send(web.settings.SMTP_SERVER)



