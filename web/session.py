import ysessions

import models.users


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
    _session = get()
    _user_notifs = _session.setdefault(USER_NOTIFS_KEY, [])
    _user_notif = UserNotif(message, level)
    _user_notifs.append(_user_notif)

def pop_user_notifs():
    return get().pop(USER_NOTIFS_KEY, [])


def login(user):
    get()[USER_ID_KEY] = user.id

def user():
    try:
        return models.users.User.read(get()[USER_ID_KEY])
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
    _session = get()
    try:
        return _session[TEMP_IMG_KEY]
    except KeyError:
        return

def save_temporary_image(image):
    _session = get()
    _session[TEMP_IMG_KEY] = image

def clean_temporary_image():
    _session = get()
    if TEMP_IMG_KEY in _session:
        del _session[TEMP_IMG_KEY]

