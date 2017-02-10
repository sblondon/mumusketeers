#! /bin/bash

. ./scripts/local/display_service.sh

PORT=8000
VERSIONIZED=`grep yversionize.VERSION web/settings.py | cut -d " " -f 3 | sed s/\"//g`

env PYTHONPATH=. ./local.virtualenv/bin/uwsgi \
    --virtualenv local.virtualenv \
    --wsgi-file ./scripts/local/run.py --http :${PORT} --need-app -b 65535 \
    --master --processes 5 --enable-threads --thunder-lock --lazy-apps \
    --static-map /media/${VERSIONIZED}=media \
    --static-map /media=media \
    --static-map /umedia=local.persistent/blobs \
    --python-auto-reload 1


