import yzodb
import models.users


class TestCreate(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create_player('User@yaal.fr')

        self.assertTrue(models.users.read("user@yaal.fr"))
        self.assertTrue(models.users.read("uSER@yaal.fr"))

    def test_once_is_enough(self):
        models.users.create_player('User@yaal.fr')

        try:
            models.users.create_player('User@yaal.fr')
            self.fail("once is enough")
        except models.NotAllowed:
            pass


class TestChangeEmail(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create_player('User@yaal.fr')
        _user.email = "UPDATE@yaal.fr"
        self.assertFalse(models.users.read("user@yaal.fr"))
        self.assertTrue(models.users.read("update@yaal.fr"))


