import yzodb
import transaction

import models.games


#class Test(yzodb.ConnectedTestCase):
#
#    def test_change_hunt(self):
#        with yzodb.connection():
#            game = models.games.create_game("whatever")
#            player_1 = game.add_player_email("player-1@domain.tld")
#            player_2 = game.add_player_email("player-2@domain.tld")
#            player_3 = game.add_player_email("player-3@domain.tld")
#            game.start()
#            #hunter, target, next_target = game.players_loop
#            
#            transaction.commit()
#
        #response = self.testapp.get(url, status=200)
        #response.click(href=web.players.forms.GhostifyPlayer.make_url(game, player))

        #with yzodb.connection():
        #    hunt = player.hunter_hunt_for_game(game)
        #    assert hunt.done_according_hunter
        #    assert False == hunt.done_according_target
        #assert 'text/html' == response.content_type
        #response.mustcontain('<!-- player home page -->')
        #response.mustcontain(player.id)


