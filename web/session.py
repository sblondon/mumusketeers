import ysessions

import models.players


USER_NOTIFS_KEY = 'user_notifs'
USER_ID_KEY = 'user_id'
TEMP_IMG_KEY = 'tmp_img'

def get():
    return ysessions.get()


class UserNotif(object):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'

    def __init__(self, message, level):
        self.message = message
        self.level = level


def add_user_info_notif(message):
    add_user_notif(message, UserNotif.INFO)

def add_user_success_notif(message):
    add_user_notif(message, UserNotif.SUCCESS)

def add_user_warning_notif(message):
    add_user_notif(message, UserNotif.WARNING)

def add_user_error_notif(message):
    add_user_notif(message, UserNotif.ERROR)

def add_user_notif(message, level):
    session = get()
    user_notifs = session.setdefault(USER_NOTIFS_KEY, [])
    user_notif = UserNotif(message, level)
    user_notifs.append(user_notif)

def pop_user_notifs():
    return get().pop(USER_NOTIFS_KEY, [])


def login(user):
    get()[USER_ID_KEY] = user.id

def user():
    try:
        return models.players.Player.read(get()[USER_ID_KEY])
    except KeyError:
        logout()

def has_user():
    return USER_ID_KEY in get()

def logout():
    try:
        del get()[USER_ID_KEY]
    except KeyError:
        pass

def temporary_image():
    session = get()
    try:
        return session[TEMP_IMG_KEY]
    except KeyError:
        return

def save_temporary_image(image):
    session = get()
    session[TEMP_IMG_KEY] = image

def clean_temporary_image():
    session = get()
    if TEMP_IMG_KEY in session:
        del session[TEMP_IMG_KEY]

