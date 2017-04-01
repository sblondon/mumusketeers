import random

import yzodb

import models


def create_game(name):
    game = Game.create()
    game.name = name
    return game


_PREPAPRING_STATUS = 0
_RUNNING_STATUS = 1

class Game(models.Model):
    table = 'games'

    name = yzodb.SimpleAttribute()
    waiting_players = yzodb.ModelSetAttribute("models.players.Player")
    playing_players = yzodb.ModelSetAttribute("models.players.Player")
    _status = yzodb.SimpleAttribute(default=_PREPAPRING_STATUS)

    def add_player_email(self, email):
        import models.players
        try:
            player = models.players.create_player(email)
        except models.NotAllowed:
            player = models.players.read(email)
        self.waiting_players.add(player)
        player.wait_for_games.add(self)
        return player

    def start(self):
        self._status = 1
        players = list(self.waiting_players)
        random.shuffle(players)
        target_loop  = {}
        for index, player in enumerate(players):
            if index == 0:
                first_player = player
                target_loop[player] = {"current target": players[index + 1]}
            elif index == len(players) - 1:
                target_loop[player] = {"current target": first_player, "targetted_by_player": players[index - 1]}
                target_loop[first_player].update({"targetted_by_player": player})
            else:
                target_loop[player] = {"current target": players[index + 1], "targetted_by_player": players[index - 1]}

        for player in players:
            self.waiting_players.remove(player)
            self.playing_players.add(player)
            player.wait_for_games.remove(self)
            player_target = target_loop[player]["current target"]
            player_hunter = target_loop[player]["targetted_by_player"]
            self._create_hunt(player_hunter, player)

    def _create_hunt(self, hunter, target):
        import models.hunts
        models.hunts.create_hunt-self, hunter, target)

    @property
    def players_loop(self):
        first_player = list(self.playing_players)[0]
        loop = [first_player]
        run_loop = True
        first_loop = True
        player = first_player.current_target_for_game(self)
        while run_loop:
            loop.append(player)
            if player == first_player and first_loop == False:
                run_loop = False
            else:
                first_loop = False
                player = player.current_target_for_game(self)
        return loop

    @property
    def preparing(self):
        return not self._status

    @property
    def running(self):
        return self._status == _RUNNING_STATUS

