import random

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
    playing_players = yzodb.ModelSetAttribute("models.users.Player")

    def add_player_email(self, email):
        import models.users
        try:
            player = models.users.create_player(email)
        except models.NotAllowed:
            player = models.users.read(email)
        self.waiting_players.add(player)
        return player

    def start(self):
        players = list(self.waiting_players)
        random.shuffle(players)
        targetting  = {}
        for index, player in enumerate(players):
            if index == 0:
                first_player = player
                targetting[player] = {"current target": players[index + 1]}
            elif index == len(players) - 1:
                targetting[player] = {"current target": first_player, "targetted_by_player": players[index - 1]}
                targetting[first_player].update({"targetted_by_player": player})
            else:
                targetting[player] = {"current target": players[index + 1], "targetted_by_player": players[index - 1]}

        for player in list(self.waiting_players):
            self.waiting_players.remove(player)
            self.playing_players.add(player)
            player.current_target = targetting[player]["current target"]
            player.targetted_by_player = targetting[player]["targetted_by_player"]

