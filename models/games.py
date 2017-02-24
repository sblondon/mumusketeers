import yzodb

import models


def create_game(name):
    game = Game.create()
    game.name = name
    return game


class Game(models.Model):
    table = 'games'

    name = yzodb.SimpleAttribute()
    waiting_players = yzodb.ModelSetAttribute("models.users.Player")

    def add_player_email(self, email):
        import models.users
        try:
            player = models.users.create_player(email)
        except models.NotAllowed:
            player = models.users.read(email)
        self.waiting_players.add(player)
        return player

