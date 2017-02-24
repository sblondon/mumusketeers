import slugid
import yzodb

import models


def create_game(name):
    game = Game.create()
    game.name = name
    return game


class Game(models.Model):
    table = 'games'

    name = yzodb.SimpleAttribute()

