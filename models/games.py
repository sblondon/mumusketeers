import yzodb
import slugid


def create_game(name):
    game = Game.create()
    game.name = name
    return game


class Game(yzodb.Model):
    table = 'games'

    name = yzodb.SimpleAttribute()


    @classmethod
    def propose_id(cls):
        return slugid.v4().decode("ascii")

