import markdownmail

import web.pages

import web.settings


class StartingGamePage(web.pages.Page):
    template = 'starting_game.md'

    def context_update(self):
        return {"game": self.game, "player": self.player}


def start_game(game):
    for player in game.playing_players:
        page = StartingGamePage()
        page.game = game
        page.player = player
        content = page.render()
        email = markdownmail.MarkdownMail(
                from_addr="noreply@changeme.tld",
                to_addr=player.email,
                subject="Game starts",
                content=content)
        email.send(web.settings.SMTP_SERVER)



