import slugid
import yzodb


class Model(yzodb.Model):

    @classmethod
    def propose_id(cls):
        return slugid.v4().decode("ascii")



class NotAllowed(Exception):
    pass

