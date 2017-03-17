import web.constantes


class AbstractGhostification:

    @classmethod
    def make_url(cls, game, player):
        return cls.action+"{game_id}/{player_id}".format(game_id=game.id, player_id=player.id)


class GhostifyPlayer(AbstractGhostification):
    action = '/game/player/ghostify/'
    action_regex = '^{action}(?P<game_id>{game_id})/(?P<player_id>{player_id})$'.format(
            action=action,
            game_id=web.constantes.SLUGID_REGEX,
            player_id=web.constantes.SLUGID_REGEX)
    method = 'GET'


class GhostifiedPlayer(AbstractGhostification):
    action = '/game/player/ghostified/'
    action_regex = '^{action}(?P<game_id>{game_id})/(?P<player_id>{player_id})$'.format(
            action=action,
            game_id=web.constantes.SLUGID_REGEX,
            player_id=web.constantes.SLUGID_REGEX)
    method = 'GET'

