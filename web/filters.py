import web.session

import random

def level_to_bootstrap_class(level):
    return {web.session.UserNotif.ERROR: 'danger'}.get(level, level)

def pretty_boolean(value):
    return "Oui" if value else "Non"

def shuffle(iterable):
    l = list(iterable)
    random.shuffle(l)
    return l

