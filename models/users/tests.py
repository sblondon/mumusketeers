import yzodb
import models.users


class TestCreate(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create('User@yaal.fr', 'password')

        self.assertTrue(models.users.read("user@yaal.fr"))
        self.assertTrue(models.users.read("uSER@yaal.fr"))

    def test_once_is_enough(self):
        models.users.create('User@yaal.fr', 'password')

        try:
            models.users.create('User@yaal.fr', 'password')
            self.fail("once is enough")
        except models.NotAllowed:
            pass


class TestChangeEmail(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create('User@yaal.fr', 'password')
        _user.email = "UPDATE@yaal.fr"
        self.assertFalse(models.users.read("user@yaal.fr"))
        self.assertTrue(models.users.read("update@yaal.fr"))


class TestAuthenticate(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create('User@yaal.fr', 'password')

        self.assertTrue(models.users.authenticate("user@Yaal.fr", 'password'))
        self.assertFalse(models.users.authenticate("user@Yaal.fr", 'wrong'))


class TestHashPassword(yzodb.ConnectedTestCase):

    def test(self):
        _user = models.users.create('user@yaal.fr', 'password')
        self.assertEquals('29141f850e2629b490a1db71d350629eecde579cae3f8885d6455bbf1dd00826', _user.password)

    def test_setter(self):
        _user = models.users.create('user@yaal.fr', 'SECRET')
        _user.password = 'password'
        self.assertEquals('29141f850e2629b490a1db71d350629eecde579cae3f8885d6455bbf1dd00826', _user.password)

