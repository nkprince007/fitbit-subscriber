#!/bin/sh

set -e

exec \
    celery worker \
    -A subscriber \
    --loglevel=$LOG_LEVEL \
    --pidfile= \
    -s /tmp/celerybeat-schedule
