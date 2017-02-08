import hashlib
import yzodb

import models
import web.session
import web.users.forms


def create(email, password):
    user = read(email)
    if user:
        raise models.NotAllowed()

    user = User.create()
    user._email = email.lower()
    user.password = password
    Indexes.add(user)
    return user

def authenticate(email, password):
    user = read(email)
    if user and user.password_equals(password):
        return user

def read(email):
    try:
        return Indexes.get(email)
    except yzodb.ObjectNotFoundException:
        return None



class User(yzodb.Model):
    table = 'users'

    _email = yzodb.SimpleAttribute()
    _password = yzodb.SimpleAttribute()

    def delete(self):
        Indexes.delete(self)
        super(User, self).delete()

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
    table = 'users_indexes'
    users_by_email = yzodb.ModelDictAttribute(model=User)

    @classmethod
    def add(cls, user):
        cls._instance().users_by_email[user.email] = user

    @classmethod
    def get(cls, email):
        return cls._instance().users_by_email[email.lower()]

    @classmethod
    def delete(cls, user):
        del cls._instance().users_by_email[user.email]

    @classmethod
    def _instance(cls):
        try:
            return next(Indexes.read_all())
        except StopIteration:
            return Indexes.create()

