#! /bin/bash

PROJECT_NAME=$(basename `pwd`)
WATCH_DIR="/tmp/${PROJECT_NAME}/tests/"
WATCH_PATH="${WATCH_DIR}watchfile"

mkdir -p ${WATCH_DIR}
./runtests $*
touch ${WATCH_PATH}
echo "watching files…"
while true ; do
  find . -not -path "./local.virtualenv/*"  -not -path "./node_modules/*" \
         \( -name "*.py" -o -name "*.html" -o -name "*.jinja" \) \
         -newer ${WATCH_PATH} \
         -exec touch ${WATCH_PATH} \; \
         -exec echo \; \
         -exec echo "run tests !" \; \
         -exec make test $* \;
  sleep 1.5
done

