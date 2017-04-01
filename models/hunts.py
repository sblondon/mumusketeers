import yzodb

import models

def create_hunt(game, hunter, target):
    hunt = Hunt.create()
    hunt.hunter = hunter
    hunt.target = target
    hunter.add_current_hunt_for_game(hunt, game)
    target.add_targetted_hunt_for_game(hunt, game)


class Hunt(models.Model):
    table = 'hunts'

    hunter = yzodb.ModelAttribute("models.players.Player")
    target = yzodb.ModelAttribute("models.players.Player")

