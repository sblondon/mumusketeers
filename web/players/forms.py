import web.constantes


class GhostifyPlayer:
    action = '/game/player/ghostify/'
    action_regex = '^{action}(?P<gameid>{gameid})/(?P<playerid>{playerid})$'.format(action=action, gameid=web.constantes.SLUGID_REGEX, playerid=web.constantes.SLUGID_REGEX)
    method = 'GET'

    @classmethod
    def make_url(cls, game, player):
        return cls.action+"{game_id}/{player_id}".format(game_id=game.id, player_id=player.id)


class GhostifiedPlayer:
    action = '/game/player/ghostified/'
    action_regex = '^{action}(?P<gameid>{gameid})/(?P<playerid>{playerid})$'.format(action=action, gameid=web.constantes.SLUGID_REGEX, playerid=web.constantes.SLUGID_REGEX)
    method = 'GET'

    @classmethod
    def make_url(cls, game, player):
        return cls.action+"{game_id}/{player_id}".format(game_id=game.id, player_id=player.id)

