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
    done_according_hunter = yzodb.BooleanAttribute()
    done_according_target = yzodb.BooleanAttribute()

    def update(self, game):
        if self.done_according_hunter and self.done_according_target:
            next_hunt = self.target.hunter_hunt_for_game(game)
            self.hunter.add_current_hunt_for_game(next_hunt, game)
            next_hunt.hunter = self.hunter
            self.target.ghostified.add(game)
