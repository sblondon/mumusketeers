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


class _ConfirmGhostifiedTemplate(web.pages.Page):
    template = 'confirm_ghostified.md'

    def context_update(self):
        return {"game": self.hunt, "hunt": self.hunt}

def request_confirm_ghostified(game, hunt):
    page = _ConfirmGhostifiedTemplate()
    page.game = game
    page.hunt = hunt
    content = page.render()
    email = markdownmail.MarkdownMail(
            from_addr="noreply@changeme.tld",
            to_addr=hunt.target.email,
            subject="Confirm you've been ghostified",
            content=content)
    email.send(web.settings.SMTP_SERVER)


class _ConfirmGhostificationTemplate(web.pages.Page):
    template = 'confirm_ghostification.md'

    def context_update(self):
        return {"game": self.hunt, "hunt": self.hunt}

def request_confirm_ghostification(game, hunt):
    page = _ConfirmGhostificationTemplate()
    page.game = game
    page.hunt = hunt
    content = page.render()
    email = markdownmail.MarkdownMail(
            from_addr="noreply@changeme.tld",
            to_addr=hunt.hunter.email,
            subject="Confirm you've ghostified a player",
            content=content)
    email.send(web.settings.SMTP_SERVER)
