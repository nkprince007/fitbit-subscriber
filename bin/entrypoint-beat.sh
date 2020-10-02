#!/bin/sh

set -e

export DB_ADDRESS=${DATABASE_SERVICE_HOST:-$DB_ADDRESS}
export DB_PORT=${DATABASE_SERVICE_PORT:-$DB_PORT}

export REDIS_ADDRESS=${REDIS_SERVICE_HOST:-$REDIS_ADDRESS}
export REDIS_PORT=${REDIS_SERVICE_PORT:-$REDIS_PORT}

echo "Waiting for database ..."
while ! pg_isready -h $DB_ADDRESS -p $DB_PORT 2>/dev/null; do
    sleep 1
done

exec \
    celery -A subscriber \
    beat \
    --loglevel=$CELERY_LOG_LEVEL \
    --pidfile= \
    -s /tmp/celerybeat-schedule
