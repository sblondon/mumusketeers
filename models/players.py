import yzodb

import models
import web.session
import web.players.forms


def create_player(email):
    player = read(email)
    if player:
        raise models.NotAllowed()

    player = Player.create()
    player._email = email.lower()
    Indexes.add(player)
    return player


def read(email):
    try:
        return Indexes.get(email)
    except yzodb.ObjectNotFoundException:
        return None


class Player(models.Model):
    table = 'players'

    _email = yzodb.SimpleAttribute()
    _current_targets = yzodb.ModelDictAttribute("models.players.Player")
    _targetted_by_players = yzodb.ModelDictAttribute("models.players.Player")

    def delete(self):
        Indexes.delete(self)
        super(Player, self).delete()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        Indexes.delete(self)
        self._email = value.lower()
        Indexes.add(self)

    def add_current_target_for_game(self, player, game):
        self._current_targets[game.id] = player

    def add_targetted_by_player_for_game(self, player, game):
        self._targetted_by_players[game.id] = player

    def current_target_for_game(self, game):
        return self._current_targets[game.id]

    def targetted_by_player_for_game(self, game):
        return self._targetted_by_players[game.id]


class Indexes(yzodb.Model):
    table = 'players_indexes'
    players_by_email = yzodb.ModelDictAttribute(model=Player)

    @classmethod
    def add(cls, player):
        cls._instance().players_by_email[player.email] = player

    @classmethod
    def get(cls, email):
        return cls._instance().players_by_email[email.lower()]

    @classmethod
    def delete(cls, user):
        del cls._instance().players_by_email[user.email]

    @classmethod
    def _instance(cls):
        try:
            return next(Indexes.read_all())
        except StopIteration:
            return Indexes.create()

