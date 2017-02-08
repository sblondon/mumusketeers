"""charge la base de donnees d'integration

with yzodb.connection():
   # code d'accès à la base"""


import web.settings
import scripts.integration.env_settings

import yzodb

yzodb.set_files_root_dir(web.settings.FILES_ROOT_DIR)
yzodb.make_connection_pool(**web.settings.CLIENT_STORAGE)

print (__doc__)

