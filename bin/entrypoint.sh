#!/bin/sh

set -e

export DB_ADDRESS=${DATABASE_SERVICE_HOST:-$DB_ADDRESS}
export DB_PORT=${DATABASE_SERVICE_PORT:-$DB_PORT}

export REDIS_ADDRESS=${REDIS_SERVICE_HOST:-$REDIS_ADDRESS}
export REDIS_PORT=${REDIS_SERVICE_PORT:-$REDIS_PORT}

while ! pg_isready -h $DB_ADDRESS -p $DB_PORT 2>/dev/null; do
    echo "Waiting for database ..."
    sleep 1
done

echo "Migrating database ..."
ENV=production python3 manage.py migrate --no-input

exec \
    gunicorn subscriber.asgi:application \
    --name=subscriber \
    --user=$APP_USER --group=$APP_USER \
    --bind=0.0.0.0:8000 \
    --log-level=$LOG_LEVEL \
    --log-file=- \
    --workers=4 \
    --worker-class=uvicorn.workers.UvicornWorker
