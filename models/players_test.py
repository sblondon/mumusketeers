import yzodb
import models.players


class TestCreate(yzodb.ConnectedTestCase):

    def test(self):
        models.players.create_player('User@yaal.fr')

        assert models.players.read("user@yaal.fr")
        assert models.players.read("uSER@yaal.fr")

    def test_once_is_enough(self):
        models.players.create_player('User@yaal.fr')

        try:
            models.players.create_player('User@yaal.fr')
            self.fail("once is enough")
        except models.NotAllowed:
            pass


class TestChangeEmail(yzodb.ConnectedTestCase):

    def test(self):
        player = models.players.create_player('User@yaal.fr')
        player.email = "UPDATE@yaal.fr"
        assert not models.players.read("user@yaal.fr")
        assert models.players.read("update@yaal.fr")


