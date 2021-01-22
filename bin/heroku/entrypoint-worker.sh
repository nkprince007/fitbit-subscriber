#!/bin/sh

set -e

exec \
    celery -A subscriber \
    worker \
    --beat \
    --loglevel=$CELERY_LOG_LEVEL \
    --pidfile= \
    -s /tmp/celerybeat-schedule
