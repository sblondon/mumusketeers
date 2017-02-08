import werkzeug

import web.settings
import scripts.local.env_settings


import web.application

application = werkzeug.SharedDataMiddleware(
       web.application.make(),
       {
           "/media/"	: "web/media/",
           "/files/"	: "local.persistent/files/",
       },
       cache=False)



