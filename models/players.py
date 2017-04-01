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
    _current_hunts = yzodb.ModelDictAttribute("models.hunts.Hunt")
    _hunted_by_players = yzodb.ModelDictAttribute("models.hunts.Hunt")
    wait_for_games = yzodb.ModelSetAttribute("models.games.Game")

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

    def current_target_for_game(self, game):
        return self._current_hunts[game.id].target

    def targetted_by_player_for_game(self, game):
        return self._hunted_by_players[game.id].hunter

    def add_current_hunt_for_game(self, hunt, game):
        self._current_hunts[game.id] = hunt

    def add_targetted_hunt_for_game(self, hunt, game):
        self._hunted_by_players[game.id] = hunt

    @property
    def games(self):
        import models.games
        games = [models.games.Game.read(game_id) for game_id in self._hunted_by_players.keys()]
        games.extend(self.wait_for_games)
        return games


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

