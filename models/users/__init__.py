import hashlib
import slugid
import yzodb

import models
import web.session
import web.users.forms


def create(email, password):
    player = read(email)
    if player:
        raise models.NotAllowed()

    player = Player.create()
    player._email = email.lower()
    player.password = password
    Indexes.add(player)
    return player

def authenticate(email, password):
    player = read(email)
    if player and player.password_equals(password):
        return player

def read(email):
    try:
        return Indexes.get(email)
    except yzodb.ObjectNotFoundException:
        return None



class Player(yzodb.Model):
    table = 'players'

    _email = yzodb.SimpleAttribute()
    _password = yzodb.SimpleAttribute()


    @classmethod
    def propose_id(cls):
        return slugid.v4().decode("ascii")

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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self._hash(value)

    def _hash(self, password):
        return hashlib.sha256('#*~/_{0}|@$%=&'.format(password).encode("utf-8")).hexdigest()

    def password_equals(self, other_password):
        return self._password == self._hash(other_password)



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

