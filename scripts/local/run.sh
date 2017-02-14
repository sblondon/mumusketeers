#! /bin/sh

. ./scripts/local/display_service.sh

OUT_DIR_PATH=./local.persistent/logs/runall
mkdir -p ${OUT_DIR_PATH}

./scripts/local/run-zeo.sh >> ${OUT_DIR_PATH}/zeo.log 2>&1 &
ZEO_PID="$!"
echo "ZEO started (pid: ${ZEO_PID}, out: ${OUT_DIR_PATH}/zeo.log)"

./scripts/local/run-wsgi.sh >> ${OUT_DIR_PATH}/uwsgi.log 2>&1 &
UWSGI_PID="$!"
echo "uWSGI RichSMS started (pid: ${UWSGI_PID}, out: ${OUT_DIR_PATH}/uwsgi.log)"


trap "kill ${UWSGI_PID} ${ZEO_PID}" EXIT INT TERM QUIT

echo "Ready"
wait
echo "Stopped"
