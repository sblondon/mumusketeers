import yzodb


def create_game(name):
    game = Game.create()
    game.name = name
    return game


class Game(yzodb.Model):
    table = 'games'

    name = yzodb.SimpleAttribute()

