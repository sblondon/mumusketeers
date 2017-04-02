import yzodb
import transaction

import models.games


def test_change_target():
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        player_3 = game.add_player_email("player-3@domain.tld")
        game.start()
        hunter, target, next_target = game.players_loop[:-1]
        hunter.declare_ghostify_for_game(game)
        transaction.commit()

    with yzodb.connection():
        assert target == hunter.current_target_for_game(game)
       
    with yzodb.connection():
        target.declare_ghostified_for_game(game)
        transaction.commit()

    with yzodb.connection():
        hunter = models.players.Player.read(hunter.id)
        assert next_target == hunter.current_target_for_game(game)
        assert hunter == hunter.hunter_hunt_for_game(game).hunter
        assert None == target.hunter_hunt_for_game(game)
        assert None == target.hunted_hunt_for_game(game)
        assert False == hunter.is_ghostified_for_game(game)
        assert target.is_ghostified_for_game(game)
        assert False == next_target.is_ghostified_for_game(game)

