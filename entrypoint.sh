#!/bin/sh
if [ $# -ne 0 ]; then
    exec "$@"
    exit $?
fi

python3 ${APP_DIR}/app.py