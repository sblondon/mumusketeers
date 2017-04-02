import yzodb
import transaction

import models.games


def test_change_target_when_target_is_the_last_declaring_ghostification():
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
        assert hunter == target.targetted_by_player_for_game(game)

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
        assert [target] == hunter.ghostified_players_for_game(game)


def test_change_target_when_hunter_is_the_last_declaring_ghostification():
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        player_3 = game.add_player_email("player-3@domain.tld")
        game.start()
        hunter, target, next_target = game.players_loop[:-1]
        target.declare_ghostified_for_game(game)
        transaction.commit()

    with yzodb.connection():
        assert target == hunter.current_target_for_game(game)
        assert hunter == target.targetted_by_player_for_game(game)

    with yzodb.connection():
        hunter.declare_ghostify_for_game(game)
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


def test_add_ghostifications():
    with yzodb.connection():
        game = models.games.create_game("whatever")
        player_1 = game.add_player_email("player-1@domain.tld")
        player_2 = game.add_player_email("player-2@domain.tld")
        player_3 = game.add_player_email("player-3@domain.tld")
        game.start()
        hunter, target, next_target = game.players_loop[:-1]

        hunter.add_ghostification_for_game(target, game)
        hunter.add_ghostification_for_game(next_target, game)
        transaction.commit()

    with yzodb.connection():
        assert [target, next_target] == hunter.ghostified_players_for_game(game)

