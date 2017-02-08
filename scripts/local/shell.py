"""charge la base de données locale

with yzodb.connection():
   # code d'accès à la base"""

from pprint import pprint
from imp import reload

import web.settings
import scripts.local.env_settings

import yzodb

yzodb.set_files_root_dir(web.settings.FILES_ROOT_DIR)
yzodb.make_connection_pool(**web.settings.CLIENT_STORAGE)

print (__doc__)

