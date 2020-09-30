#!/bin/sh

set -e

exec \
    celery -A subscriber \
    worker \
    --loglevel=$LOG_LEVEL \
    --pidfile= \
    -s /tmp/celerybeat-schedule
