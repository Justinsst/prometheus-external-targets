#!/bin/sh
if [ $# -ne 0 ]; then
    exec "$@"
    exit $?
fi

poetry run python3 -m external_targets.main