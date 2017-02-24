import yzodb

import models
import web.session
import web.users.forms


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

